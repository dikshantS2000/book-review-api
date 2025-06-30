from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session
from app.model import Book, Review
from app.database import get_session
from app.cache import get_reviews_from_cache, set_reviews_in_cache
from fastapi.responses import JSONResponse

router = APIRouter()

#API to GET all the books in the DB
@router.get("/books", response_model=list[Book])
def list_books(session: Session = Depends(get_session)):
    books = session.exec(select(Book)).all()
    return books


#API to add a new book to the DB
@router.post("/books", response_model=Book)
def create_book(book: Book, session: Session = Depends(get_session)):
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

#API to GET a book review based on BookID
@router.get("/books/{book_id}/reviews", response_model=list[Review])
def get_reviews(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    #Caching using Redis
    cached = get_reviews_from_cache(book_id)
    if cached is not None:
        return JSONResponse(content=cached)

    #Caching if Redis fails
    reviews = session.exec(select(Review).where(Review.book_id == book_id)).all()

    set_reviews_in_cache(book_id, [r.model_dump() for r in reviews]
)

    return reviews


#API to add a review about any book
@router.post("/books/{book_id}/reviews", response_model=Review)
def add_review(book_id: int, review: Review, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    review.book_id = book_id
    session.add(review)
    session.commit()
    session.refresh(review)
    return review
