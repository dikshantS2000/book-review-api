#Book Review Backend API

This is a simple Book Review backend service built using **FastAPI**, **SQLModel**, **SQLite**, and **Redis**. It supports storing books and their reviews, and uses Redis caching to optimize performance.

---

##Features

-Add and list books
-Add and fetch reviews for a book
-Redis cache integration for fast review lookups
-OpenAPI (Swagger) documentation
-Automated unit and integration tests using `pytest`

---

##Project Structure

Python Backend Assessment/
├── app/
│ ├── init.py
│ ├── main.py # FastAPI app entrypoint
│ ├── route.py # API routes
│ ├── database.py # DB engine and session
│ ├── model.py # SQLModel models
├── test/
│ ├── init.py
│ └── test_api.py # Unit & integration tests
├── redis-x64-5.x.x/ # Redis (if installed manually)
├── books.db # SQLite DB (auto-created)
└── README.md


---

##Setup Instructions

1.Clone the Repository

```
https://github.com/dikshantS2000/book-review-api.git
cd book-review-api
```

2.Create & Activate Virtual Environment (Optional but recommended)

```
python -m venv venv
venv\Scripts\activate  # On Windows
```
3. Install Dependencies

```
pip install -r requirements.txt
```

##Redis Setup (Windows)

Option 1: Redis for Windows

If Redis is not running, start it manually:
```
cd redis-x64-5.x.x
redis-server.exe redis.windows.conf
```
Make sure port 6379 is available.

Run the Application

```
uvicorn app.main:app --reload
```

Visit the docs:

Swagger UI: http://localhost:8000/docs

Redoc: http://localhost:8000/redoc

##Run Tests

Make sure Redis is running before testing:
```
redis-server.exe redis.windows.conf
```
Then from the root directory:
```
set PYTHONPATH=. && pytest
```


Author
Dikshant Sharma
