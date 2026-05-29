from fastapi import *
from pydantic import *
from typing import *

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(
        description="Id is not needed to create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)

    model_config = {
        "jsnon_shcema_ectra": {
            "example": {
                "title": "A new Book",
                "author": "Mchael Sweeny",
                "description": "A new description",
                "rating": "5"
            }
        }
    }


BOOKS = [
    Book(1, "Introductory Software Engineering",
         "Michael Sweeney", "Very Good Introduction", "5"),
    Book(2, "Essential Machine Learning", "John Doe",
         "In depth intro to Machine Learning", "4"),
    Book(3, "Computers for Dummies", "Jane Smith",
         "Learn computer science for dummies", "3"),
    Book(4, "Master Neural Networks", "Arthur Kernis",
         "Advanced topics of neural networks", "5"),
    Book(5, "Larping 101", "Clav", "How to larp", "5"),
    Book(6, "Land an internship", "James Graham",
         "All you need to know about getting internships at top companies", "4")
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
