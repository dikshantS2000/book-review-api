from sqlmodel import SQLModel, create_engine, Session
from app.model import Book, Review

DATABASE_URL = "sqlite:///./books.db"
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)

if __name__ == "__main__":
    init_db()
