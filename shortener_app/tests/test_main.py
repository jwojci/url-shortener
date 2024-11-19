import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shortener_app.main import app, get_db
from shortener_app.db import Base
from shortener_app.config import get_settings

# Create a test database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@db:5432/xberrytask"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert (
        response.status_code == 200
    ), f"Expected 200 but got {response.status_code} for response: {response.text}"
    assert "URL Shortener" in response.text


def test_shorten_url_valid():
    response = client.post(
        "/shorten_url", data={"target_url": "https://www.example.com"}
    )
    assert response.status_code == 200

    assert "Shortened URL:" in response.text


def test_shorten_url_invalid():
    response = client.post("/shorten_url", data={"target_url": "not_a_valid_url"})
    assert (
        response.status_code == 400
    ), f"Expected 400 but got {response.status_code} for response: {response.text}"
    assert "Your provided URL is not valid" in response.text


def test_redirect_to_target_url():
    # create a shortened URL
    shorten_response = client.post(
        "/shorten_url", data={"target_url": "https://www.google.com"}
    )
    assert shorten_response.status_code == 200

    assert "Shortened URL:" in shorten_response.text

    # get the short_url from the HTML response
    short_url_start = shorten_response.text.find('href="') + len('href="')
    short_url_end = shorten_response.text.find('"', short_url_start)
    short_url = shorten_response.text[short_url_start:short_url_end]

    short_code = short_url.split("/")[-1]

    # Test the redirection
    redirect_response = client.get(f"/{short_code}", allow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == "https://www.google.com"


def test_redirect_nonexistent_url():
    response = client.get("/nonexistent", allow_redirects=False)
    assert response.status_code == 404
    assert "Short url not found" in response.text
