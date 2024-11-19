from sqlalchemy.orm import Session
from sqids import Sqids

from . import models
from .config import get_settings

sqids = Sqids(
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    min_length=6,
)


def get_short_url(db: Session, url: str):
    # check if target_url has already been encoded
    existing_url = db.query(models.URL).filter(models.URL.target_url == url).first()
    if existing_url:
        return existing_url.short_url

    # if not already encoded, proceed to encode it and save it
    new_url = models.URL(target_url=url)
    db.add(new_url)
    db.flush()

    short_url_key = sqids.encode([new_url.id])
    new_url.key = short_url_key

    base_url = get_settings().base_url
    short_url = f"{base_url}/{short_url_key}"
    new_url.short_url = short_url

    db.commit()
    db.refresh(new_url)
    return short_url


def get_target_url(db: Session, url: str):
    url_record = db.query(models.URL).filter(models.URL.key == url).first()
    if url_record:
        return url_record.target_url
    else:
        return None
