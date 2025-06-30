from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id", index=True)
    rating: int
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Define relationship here
    book: Optional["Book"] = Relationship(back_populates="reviews")


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    reviews: List[Review] = Relationship(back_populates="book")
