from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from app.repositories.url_repository import UrlRepository
from app.database import get_db
from app.services.url_shortener import UrlShortener
from app.services.custom import CustomAliasStrategy
from sqlalchemy.orm import Session
import app.cons as constants
from app import schemas
import app.models

router = APIRouter()

@router.get(
    "/", 
    response_model = schemas.HealthCheckResponse,
    status_code = status.HTTP_200_OK
)
def health_check() -> schemas.HealthCheckResponse | JSONResponse:
    return schemas.HealthCheckResponse(status_code=200, msg="Server is healthy!")

@router.post(
    "/shorten", 
    response_model=schemas.UrlView,
    status_code=status.HTTP_201_CREATED
)
def shorten_url(
    request: schemas.ShortenRequestBody, 
    db: Session = Depends(get_db),
    ):

    repo = UrlRepository(db)
    selected_strategy = constants.STRATEGY_MAP.get(request.strategy)
    
    if not selected_strategy:
        raise HTTPException(status_code=400, detail="Invalid strategy.")
    
    shortener = UrlShortener(repo, selected_strategy)
    
    # Add custom_code param if CustomAlias is used
    try:
        shorten_code = shortener.shorten_url(
            request.original_url,
            request.custom_code if isinstance(selected_strategy, CustomAliasStrategy) else None 
        )

        record: app.models.Url | None = shortener.get_url_record(shorten_code)
        return record
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{short_code}", status_code=status.HTTP_301_MOVED_PERMANENTLY)
def get_redirect_url(
    short_code: str, 
    request: Request, 
    db: Session = Depends(get_db)
    ):

    repo = UrlRepository(db)
    url_shortener = UrlShortener(repo, strategy=None)
    original_url = url_shortener.expand_url(short_code=short_code)

    if original_url:
        url_shortener.track_url_access(
            short_code = short_code,
            ip_address = request.client.host,
            user_agent = request.headers.get("user-agent")
        )
        return RedirectResponse(url=original_url)
    return {"error": "URL not found"}

@router.get(
    "/{short_code}/info",
    response_model = schemas.UrlAnalyticsView,
    status_code=status.HTTP_200_OK
)
def get_analytics(
    short_code: str, 
    db: Session = Depends(get_db),
    ):

    repo = UrlRepository(db)
    url_analytics: app.models.UrlAnalytics | None = repo.get_url_analytics(short_code)
    return url_analytics

@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analytics(short_code: str, db: Session = Depends(get_db)) -> JSONResponse:
    repo = UrlRepository(db)
    if repo.delete_short_url(short_code):
        return JSONResponse({"message": f"Short code {short_code} has been deleted."})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Short code not found.") 