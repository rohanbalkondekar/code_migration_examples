from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI()

# In-memory database
books_db = []


class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    published_year: int


@app.post("/books/", response_model=Book)
def create_book(book: Book):
    book.id = len(books_db) + 1
    books_db.append(book)
    return book


@app.get("/books/", response_model=List[Book])
def read_books():
    return books_db


@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            updated_book.id = book_id
            books_db[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", response_model=dict)
def delete_book(book_id: int):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            del books_db[i]
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
