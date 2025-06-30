from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app
from app.database import init_db
import pytest
import redis

client = TestClient(app)

#To Make sure DB tables exist
init_db()

@pytest.fixture(scope="module", autouse=True)
def clear_redis():
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    r.flushall()
    yield
    r.flushall()

def test_create_book():
    response = client.post("/books", json={
        "title": "1984",
        "author": "George Orwell"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "1984"
    assert "id" in data

def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_review_and_cache_miss():
    book_id = 1
    review_data = {
        "rating": 5,
        "comment": "Classic dystopia!"
    }
    response = client.post(f"/books/{book_id}/reviews", json=review_data)
    assert response.status_code == 200

    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    r.delete(f"book:{book_id}:reviews")

    response = client.get(f"/books/{book_id}/reviews")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
