from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from . import config as cfg

engine = create_engine(cfg.get_settings().database_url, connect_args = {"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

# Generator for dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback
        raise e
    finally:
        db.close()