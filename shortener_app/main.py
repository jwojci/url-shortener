import validators
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from celery.result import AsyncResult
from pathlib import Path

from .celery_tasks import shorten_url_task
from .db import get_db, Base, engine
from . import schemas
from .crud import get_target_url

# create tables in db
Base.metadata.create_all(bind=engine)

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/shorten_url")
async def shorten_url(
    request: Request, url: schemas.URLInput = Form(...), db: Session = Depends(get_db)
):

    if not validators.url(url.target_url):
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "Your provided URL is not valid"},
            status_code=400,
        )

    try:
        task = shorten_url_task.delay(url.target_url)
        short_url = AsyncResult(task.id).get(timeout=10)
        return templates.TemplateResponse(
            request=request, name="index.html", context={"short_url": short_url}
        )
    except TimeoutError:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": "URL shortening is taking longer than expected. Please try again."
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            request=request, name="index.html", context={"error": str(e)}
        )


@app.get("/{short_code}")
async def redirect_to_target_ulr(short_code: str, db: Session = Depends(get_db)):
    target_url = get_target_url(db, short_code)
    if target_url:
        return RedirectResponse(url=target_url)
    else:
        raise HTTPException(status_code=404, detail="Short url not found")
