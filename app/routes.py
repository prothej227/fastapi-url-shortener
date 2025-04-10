from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from app.repositories.url_repository import UrlRepository
from app.database import get_db
from app.services.url_shortener import UrlShortener
from app.services.custom import CustomAliasStrategy
from sqlalchemy.orm import Session
import app.cons as constants
from app import schemas
from app import models
from app.services.auth import get_current_user
from typing import Optional, List

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
    current_user: models.User = Depends(get_current_user)
    ):

    repo = UrlRepository(db)

    try:
        strategy_enum = constants.StrategyType(tuple([request.strategy]))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid strategy.")
    
    print(strategy_enum)

    selected_strategy: constants.StrategyType = constants.STRATEGY_MAP.get(strategy_enum)
    
    shortener = UrlShortener(repo, selected_strategy)
    
    # Add custom_code param if CustomAlias is used
    shorten_code = shortener.shorten_url(
        request.original_url,
        current_user,
        request.custom_code if isinstance(selected_strategy, CustomAliasStrategy) else None 
    )

    if shorten_code is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="URL has already been shortened.")
    
    record: models.Url | None = shortener.get_url_record(shorten_code)
    return record
    
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
    response_model = Optional[List[schemas.UrlAnalyticsView]],
    status_code=status.HTTP_200_OK
)
def get_analytics(
    short_code: str, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    ):
    repo = UrlRepository(db)
    url_analytics = repo.get_url_analytics(short_code)
    if not url_analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No analytics found for code {short_code}"
        )
    return url_analytics

@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analytics(
    short_code: str, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> JSONResponse:
    repo = UrlRepository(db)
    if repo.delete_short_url(short_code):
        return JSONResponse({"message": f"Short code {short_code} has been deleted."})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Short code not found.")

@router.get("/get_user_urls", status_code=status.HTTP_200_OK)
def get_user_urls(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    repo = UrlRepository(db)
    return repo.get_urls_by_user