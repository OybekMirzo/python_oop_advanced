from dataclasses import dataclass

@dataclass
class Book:
    title: str
    author: str
    pages: int

book1 = Book("Atomic Habits", "James Clear", 320 )
book2 = Book("Atomic Habits", "James Clear", 320 )

print(book1)
print(book1 == book2)