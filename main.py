from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os

# Database configuration
DATABASE_URL = "postgresql://abdo1:fullstack1@localhost:5435/library_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)
    publication_year = Column(Integer)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    borrowings = relationship("Borrowing", back_populates="book")

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    address = Column(Text)
    membership_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    borrowings = relationship("Borrowing", back_populates="member")

class Borrowing(Base):
    __tablename__ = "borrowings"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    is_returned = Column(Boolean, default=False)
    
    book = relationship("Book", back_populates="borrowings")
    member = relationship("Member", back_populates="borrowings")

# Pydantic Models
class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    category: str
    publication_year: int
    total_copies: int = 1
    description: Optional[str] = None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    category: str
    publication_year: int
    total_copies: int
    available_copies: int
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class MemberCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    membership_date: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class BorrowingCreate(BaseModel):
    book_id: int
    member_id: int
    due_date: datetime

class BorrowingResponse(BaseModel):
    id: int
    book_id: int
    member_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    is_returned: bool
    book: BookResponse
    member: MemberResponse
    
    class Config:
        from_attributes = True

# FastAPI App
app = FastAPI(title="Library Management System", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Book endpoints
@app.get("/books", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict(), available_copies=book.total_copies)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}

# Member endpoints
@app.get("/members", response_model=List[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    members = db.query(Member).all()
    return members

@app.get("/members/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@app.post("/members", response_model=MemberResponse)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    db_member = Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

@app.put("/members/{member_id}", response_model=MemberResponse)
def update_member(member_id: int, member: MemberCreate, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    for key, value in member.dict().items():
        setattr(db_member, key, value)
    
    db.commit()
    db.refresh(db_member)
    return db_member

@app.delete("/members/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    db.delete(db_member)
    db.commit()
    return {"message": "Member deleted successfully"}

# Borrowing endpoints
@app.get("/borrowings", response_model=List[BorrowingResponse])
def get_borrowings(db: Session = Depends(get_db)):
    borrowings = db.query(Borrowing).all()
    return borrowings

@app.post("/borrowings", response_model=BorrowingResponse)
def create_borrowing(borrowing: BorrowingCreate, db: Session = Depends(get_db)):
    # Check if book is available
    book = db.query(Book).filter(Book.id == borrowing.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book not available")
    
    # Check if member exists
    member = db.query(Member).filter(Member.id == borrowing.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Create borrowing
    db_borrowing = Borrowing(**borrowing.dict())
    db.add(db_borrowing)
    
    # Update available copies
    book.available_copies -= 1
    
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing

@app.put("/borrowings/{borrowing_id}/return")
def return_book(borrowing_id: int, db: Session = Depends(get_db)):
    borrowing = db.query(Borrowing).filter(Borrowing.id == borrowing_id).first()
    if not borrowing:
        raise HTTPException(status_code=404, detail="Borrowing not found")
    
    if borrowing.is_returned:
        raise HTTPException(status_code=400, detail="Book already returned")
    
    # Update borrowing
    borrowing.return_date = datetime.utcnow()
    borrowing.is_returned = True
    
    # Update available copies
    book = db.query(Book).filter(Book.id == borrowing.book_id).first()
    book.available_copies += 1
    
    db.commit()
    return {"message": "Book returned successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
