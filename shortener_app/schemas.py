from pydantic import BaseModel, HttpUrl


class URLInput(BaseModel):
    target_url: str


class URLShortened(BaseModel):
    short_url: str
