from cryptography.fernet import Fernet
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import date
from decimal import Decimal

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# Section схемы
class SectionBase(BaseModel):
    section_name: str = Field(..., max_length=100)

class SectionCreate(SectionBase):
    pass

class Section(SectionBase):
    section_id: int

    class Config:
        orm_mode = True

# Rack схемы
class RackBase(BaseModel):
    rack_name: str = Field(..., max_length=100)
    section_id: int

class RackCreate(RackBase):
    pass

class Rack(RackBase):
    rack_id: int
    section: Optional[Section]

    class Config:
        orm_mode = True

# Shelf схемы
class ShelfBase(BaseModel):
    shelf_number: int
    rack_id: int

class ShelfCreate(ShelfBase):
    pass

class Shelf(ShelfBase):
    shelf_id: int
    rack: Optional[Rack]

    class Config:
        orm_mode = True

# Author схемы
class AuthorBase(BaseModel):
    author_lname: str = Field(..., max_length=100)
    author_fname: str = Field(..., max_length=100)
    author_mname: Optional[str] = Field(None, max_length=100)
    birth_year: int
    death_year: Optional[int]

    @field_validator('birth_year')
    def check_year(cls, value, field):
        if value and value > date.today().year:
            raise ValueError(f'{field.name} cannot be in the future')
        return value

    @field_validator('death_year')
    def check_death_year(cls, death_year, values):
        if death_year and 'birth_year' in values and death_year <= values['birth_year']:
            raise ValueError('death_year must be greater than birth_year')
        return death_year

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    author_id: int

    class Config:
        orm_mode = True

# Genre схемы
class GenreBase(BaseModel):
    genre_name: str = Field(..., max_length=100)

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    genre_id: int

    class Config:
        orm_mode = True

# Category схемы
class CategoryBase(BaseModel):
    category_name: str = Field(..., max_length=100)

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    category_id: int

    class Config:
        orm_mode = True

# Publisher схемы
class PublisherBase(BaseModel):
    publisher_name: str = Field(..., max_length=100)

class PublisherCreate(PublisherBase):
    pass

class Publisher(PublisherBase):
    publisher_id: int

    class Config:
        orm_mode = True

# Book схемы
class BookBase(BaseModel):
    book_name: str = Field(..., max_length=255)
    publishing_year: int
    pages_number: int
    loaned: bool
    category_id: int
    publisher_id: int

class BookCreate(BookBase):
    pass

class BookCopyCreateSchema(BaseModel):
    photo: Optional[str] = None
    book_name: str
    publisher_name: str
    shelf_id: int = 11

class BookCreateSchema(BaseModel):
    book_name: str
    publishing_year: int
    pages_number: int
    category_name: str
    genre_name: str
    author_lname: str
    author_fname: str
    author_mname: Optional[str] = None
    birth_year: int
    death_year: Optional[int] = None

class Book(BookBase):
    book_id: int
    category: Optional[Category]
    publisher: Optional[Publisher]

    class Config:
        orm_mode = True

# BookCopy схемы
class BookCopyBase(BaseModel):
    book_name: str = Field(..., max_length=255, description='Название книги')
    publishing_year: int = Field(..., gt=100, description='Год издания')
    pages_number: int = Field(..., gt=100, description='Количество страниц')
    category: str = Field(..., max_length=100, description='Категория')
    genre: str = Field(..., max_length=100, description='Жанр')
    publisher: str = Field(..., max_length=100, description='Издатель')

class BookCopyUpdateSchema(BaseModel):
    status: Optional[str] = None

class BookCopyCreate(BookCopyBase):
    pass

class BookCopy(BookCopyBase):
    copy_id: int

    class Config:
        orm_mode = True

class BookCopyInfo(BaseModel):
    copy_id: int
    book: str
    genre: str
    author: List[str]
    book_location: Optional[str]
    photo: Optional[str] = None
    status: str

# BookLocation схемы
class BookLocationBase(BaseModel):
    shelf_id: int
    book_id: int

class BookLocationCreate(BookLocationBase):
    pass

class BookLocation(BookLocationBase):
    shelf: Optional[Shelf]
    book: Optional[Book]

    class Config:
        orm_mode = True

# AuthorBook схемы
class AuthorBookBase(BaseModel):
    author_id: int
    book_id: int

class AuthorBookCreate(AuthorBookBase):
    pass

class AuthorBook(AuthorBookBase):
    author: Optional[Author]
    book: Optional[Book]

    class Config:
        orm_mode = True

# GenreBook схемы
class GenreBookBase(BaseModel):
    genre_id: int
    book_id: int

class GenreBookCreate(GenreBookBase):
    pass

class GenreBook(GenreBookBase):
    genre: Optional[Genre]
    book: Optional[Book]

    class Config:
        orm_mode = True

# Loan схемы
class LoanBase(BaseModel):
    due_date: date
    book_name: str
    user_id: int

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    loan_id: int
    book: Optional[Book]

    class Config:
        orm_mode = True

# Reader схемы
class ReaderBase(BaseModel):
    user_lname: str = Field(..., max_length=100)
    user_fname: str = Field(..., max_length=100)
    user_mname: Optional[str] = Field(None, max_length=100)
    user_passport_series: int = Field(..., ge=1000, le=9999)
    user_passport_number: int = Field(..., ge=100000, le=999999)
    user_email: str = Field(..., max_length=100)
    status: str = Field('Активный')
    photo: str = Field(..., max_length=100)

class ReaderUpdate(BaseModel):
    user_lname: Optional[str] = None
    user_fname: Optional[str] = None
    user_mname: Optional[str] = None
    user_passport_series: Optional[int] = None
    user_passport_number: Optional[int] = None
    user_email: Optional[str] = None
    status: Optional[str] = None
    photo: Optional[str] = None

    class Config:
        orm_mode = True

class ReaderDelete(BaseModel):
    user_lname: Optional[str] = None
    user_fname: Optional[str] = None
    user_mname: Optional[str] = None
    user_passport_series: Optional[int] = None
    user_passport_number: Optional[int] = None
    user_email: Optional[str] = None
    status: Optional[str] = None
    photo: Optional[str] = None

class ReaderCreate(ReaderBase):
    pass

class Reader(ReaderBase):
    user_id: int

    class Config:
        orm_mode = True

class User(BaseModel):
    username: str
    # email: str | None = None
    # full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

class UserInfo(BaseModel):
    user_id: int
    user_name: str
    user_email: str
    registration_date: date
    borrowed_books: List[str]
    fines: Optional[Decimal] = None
    status: str

class FineBase(BaseModel):
    user_lname: str = Field(..., max_length=100)
    user_fname: str = Field(..., max_length=100)
    user_mname: Optional[str] = Field(..., max_length=100)
    date_received: date
    book: str
    status: str

class FineCreate:
    pass

class Fine(FineBase):
    id: int

    class Config:
        orm_mode = True

class FineUpdate(BaseModel):
    fine_amount: Optional[Decimal] = None
    fine_date: Optional[date] = None
    fine_paid: Optional[bool] = None
    user_id: Optional[int] = None

    class Config:
        orm_mode = True

class FineInfo(BaseModel):
    fine_id: int
    user_name: str
    user_email: str
    fine_amount: Decimal
    date_received: date
    unreturned_books: List[str]
    paid: bool

# LoanHistory схемы
class LoanHistoryBase(BaseModel):
    loan_id: int
    member_id: int

class LoanHistoryCreate(LoanHistoryBase):
    pass

class LoanHistory(LoanHistoryBase):
    loan: Optional[Loan]
    member: str

    class Config:
        orm_mode = True