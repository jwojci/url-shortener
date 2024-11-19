from celery import Celery
from sqlalchemy.orm import Session

from .config import get_settings
from .crud import get_short_url
from .db import SessionLocal
from .schemas import URLInput

celery_app = Celery(
    "shortener_app",
    broker=get_settings().redis_broker_url,
    backend=get_settings().redis_backend_url,
)


@celery_app.task
def shorten_url_task(target_url: str):
    db = SessionLocal()
    try:
        short_url = get_short_url(db, target_url)
        return short_url
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
