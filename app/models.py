from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey, CheckConstraint, UniqueConstraint, \
    Numeric, TIMESTAMP, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Schema: library_schema

class Section(Base):
    __tablename__ = 'sections'
    __table_args__ = (
        UniqueConstraint('section_name'),
        {'schema': 'library_schema'}
    )
    section_id = Column(Integer, primary_key=True, default='Основной склад')
    section_name = Column(String(100), nullable=False)

class Rack(Base):
    __tablename__ = 'racks'
    __table_args__ = (
        CheckConstraint('length(rack_name) <= 100'),
        {'schema': 'library_schema'}
    )
    rack_id = Column(Integer, primary_key=True)
    rack_name = Column(String(100), nullable=False, default='На складе')
    section_id = Column(Integer, ForeignKey('library_schema.sections.section_id'), nullable=False)

    section = relationship('Section', back_populates='racks')

Section.racks = relationship('Rack', order_by=Rack.rack_id, back_populates='section')

class Shelf(Base):
    __tablename__ = 'shelfs'
    __table_args__ = (
        UniqueConstraint('shelf_number', 'rack_id'),
        CheckConstraint('length(shelf_number) > 0'),
        {'schema': 'library_schema'}
    )
    shelf_id = Column(Integer, primary_key=True)
    shelf_number = Column(String(100), nullable=False, default='На складе')
    rack_id = Column(Integer, ForeignKey('library_schema.racks.rack_id'), nullable=False)

    rack = relationship('Rack', back_populates='shelfs')

Rack.shelfs = relationship('Shelf', back_populates='rack')

class Author(Base):
    __tablename__ = 'authors'
    __table_args__ = (
        CheckConstraint('length(author_lname) <= 100'),
        CheckConstraint('length(author_fname) <= 100'),
        CheckConstraint('length(author_mname) <= 100'),
        CheckConstraint('length(author_sname) <= 100'),
        CheckConstraint('birth_year > 0 AND birth_year <= extract(year from author_now()))'),
        CheckConstraint('death_year > birth_year AND death_year <= extract(year from author_now()))'),
        {'schema': 'library_schema'}
    )
    author_id = Column(Integer, primary_key=True)
    author_lname = Column(String(100), nullable=False)
    author_fname = Column(String(100), nullable=False)
    author_mname = Column(String(100))
    birth_year = Column(Integer, nullable=False)
    death_year = Column(Integer)

class Genre(Base):
    __tablename__ = 'genres'
    __table_args__ = (
        UniqueConstraint('genre_name'),
        CheckConstraint('length(genre_name) <= 100'),
        {'schema': 'library_schema'}
    )
    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String(100), nullable=False, unique=True)

class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        UniqueConstraint('category_name'),
        CheckConstraint('length(category_name) <= 100'),
        {'schema': 'library_schema'}
    )
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(100), nullable=False)

class Publisher(Base):
    __tablename__ = 'publishers'
    __table_args__ = (
        UniqueConstraint('publisher_name'),
        CheckConstraint('length(publisher_name) <= 100'),
        {'schema': 'library_schema'}
    )
    publisher_id = Column(Integer, primary_key=True)
    publisher_name = Column(String(100), nullable=False)

class Book(Base):
    __tablename__ = 'books'
    __table_args__ = (
        CheckConstraint('length(book_name) <= 255'),
        CheckConstraint('publishing_year > 0 AND publishing_year <= extract(year from book_now()))'),
        CheckConstraint('pages_number > 0'),
        {'schema': 'library_schema'}
    )
    book_id = Column(Integer, primary_key=True)
    book_name = Column(String(255), nullable=False)
    publishing_year = Column(Integer, nullable=False)
    pages_number = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('library_schema.categories.category_id'), nullable=False)
    genre_id = Column(Integer, ForeignKey('library_schema.genres.genre_id'), nullable=False)

    category = relationship('Category', back_populates='books')
    genre = relationship('Genre', back_populates='books')

Genre.books = relationship('Book', order_by=Book.book_id, back_populates='genre')
Category.books = relationship('Book', order_by=Book.book_id, back_populates='category')

class AuthorBook(Base):
    __tablename__ = 'authors_books'
    __table_args__ = (
        {'schema': 'library_schema'},
    )
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('library_schema.authors.author_id'), nullable=False)
    book_id = Column(Integer, ForeignKey('library_schema.books.book_id'), nullable=False)

    author = relationship('Author', back_populates='authors_books')
    book = relationship('Book', back_populates='authors_books')

Author.authors_books = relationship('AuthorBook', back_populates='author')
Book.authors_books = relationship('AuthorBook', back_populates='book')

class BookCopy(Base):
    __tablename__ = 'book_copies'
    __table_args__ = (
        CheckConstraint("status IN  ('Доступна', 'На руках', 'Повреждена', 'Утеряна')"),
        {'schema': 'library_schema'}
    )
    copy_id = Column(Integer, primary_key=True)
    photo = Column(String(255))
    status = Column(String, nullable=False, default='Доступна')
    book_id = Column(Integer, ForeignKey('library_schema.books.book_id'), nullable=False)
    publisher_id = Column(Integer, ForeignKey('library_schema.publishers.publisher_id'), nullable=False)

    book = relationship('Book', back_populates='book_copies')
    publisher = relationship('Publisher', back_populates='book_copies')

Book.book_copies = relationship('BookCopy', order_by=BookCopy.copy_id, back_populates='book')
Publisher.book_copies = relationship('BookCopy', order_by=BookCopy.copy_id, back_populates='publisher')

class BookLocation(Base):
    __tablename__ = 'book_locations'
    __table_args__ = (
        {'schema': 'library_schema'},
    )
    id = Column(Integer, primary_key=True)
    shelf_id = Column(Integer, ForeignKey('library_schema.shelfs.shelf_id'), nullable=False)
    copy_id = Column(Integer, ForeignKey('library_schema.book_copies.copy_id'), nullable=False)

    shelf = relationship('Shelf', back_populates='book_locations')
    copy = relationship('BookCopy', back_populates='book_locations')

Shelf.book_locations = relationship('BookLocation', back_populates='shelf')
BookCopy.book_locations = relationship('BookLocation', back_populates='copy')

class Loan(Base):
    __tablename__ = 'loans'
    __table_args__ = (
        CheckConstraint('due_date > loan_date'),
        CheckConstraint('return_date >= loan_date'),
        {'schema': 'library_schema'}
    )
    loan_id = Column(Integer, primary_key=True)
    loan_date = Column(Date, nullable=False, server_default=func.current_date())
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)
    copy_id = Column(Integer, ForeignKey('library_schema.book_copies.book_id'), nullable=False)

    copy = relationship('BookCopy', back_populates='loans')

BookCopy.loans = relationship('Loan', order_by=Loan.loan_id, back_populates='copy')

class UserCard(Base):
    __tablename__ = 'user_cards'
    __table_args__ = (
        UniqueConstraint('user_email'),
        CheckConstraint('length(user_lname) <= 100'),
        CheckConstraint('length(user_fname) <= 100'),
        CheckConstraint('length(user_mname) <= 100'),
        CheckConstraint('user_passport_series BETWEEN 1000 AND 9999'),
        CheckConstraint('user_passport_number BETWEEN 100000 AND 999999'),
        CheckConstraint("length(user_email) <= 255 AND user_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'"),
        CheckConstraint("status IN ('Активный', 'Неактивный')"),
        {'schema': 'library_schema'},
    )
    user_id = Column(Integer, primary_key=True)
    user_lname = Column(String(100), nullable=False)
    user_fname = Column(String(100), nullable=False)
    user_mname = Column(String(100))
    user_passport_series = Column(Integer, nullable=False)
    user_passport_number = Column(Integer, nullable=False)
    user_email = Column(String(255), nullable=False)
    status = Column(String, nullable=False)
    photo = Column(String(255))
    registration_date = Column(Date, nullable=False, server_default=func.current_date())
    loan_id = Column(Integer, ForeignKey('library_schema.loans.loan_id'), nullable=False)

    loan = relationship('Loan', back_populates='user_cards')

Loan.user_cards = relationship('UserCard', order_by=UserCard.user_id, back_populates='loan')

class Fine(Base):
    __tablename__ = 'fines'
    __table_args__ = (
        CheckConstraint('fine_amount >= 100'),
        {'schema': 'library_schema'},
    )
    fine_id = Column(Integer, primary_key=True)
    fine_amount = Column(Numeric(10,2), nullable=False)
    fine_date = Column(Date, nullable=False, server_default=func.current_date())
    fine_paid = Column(Boolean, nullable=False, default=False)
    user_id = Column(Integer, ForeignKey('library_schema.user_cards.user_id'), nullable=False)

    user = relationship('UserCard', back_populates='fines')

UserCard.fines = relationship('Fine', order_by=Fine.fine_id, back_populates='user', cascade='all, delete-orphan')

class FineCard(Base):
    __tablename__ = 'fines_cards'
    __table_args__ = (
        {'schema': 'library_schema'},
    )
    id = Column(Integer, primary_key=True)
    fine_id = Column(Integer, ForeignKey('library_schema.fines.fine_id'))
    user_id = Column(Integer, ForeignKey('library_schema.user_cards.user_id'))

    fine = relationship('Fine', back_populates='fines_cards')
    user = relationship('UserCard', back_populates='fines_cards')

Fine.fines_cards = relationship('FineCard', order_by=FineCard.fine_id, back_populates='fine', cascade='all, delete-orphan')
UserCard.fines_cards = relationship('FineCard', order_by=FineCard.user_id, back_populates='user')

class CardLog(Base):
    __tablename__ = 'card_logs'
    __table_args__ = (
        {'schema': 'db_logs'},
    )
    card_log_id = Column(Integer, primary_key=True)
    card_id = Column(Integer, nullable=False)
    table_field = Column(String, nullable=False)
    operation_type = Column(String, nullable=False)
    prev_value = Column(String, nullable=False)
    new_value = Column(String, nullable=False)
    change_time = Column(TIMESTAMP, nullable=False, server_default=func.now())

class BookLog(Base):
    __tablename__ = 'book_logs'
    __table_args__ = (
        {'schema': 'db_logs'},
    )
    book_log_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    table_field = Column(String, nullable=False)
    operation_type = Column(String, nullable=False)
    prev_value = Column(String, nullable=False)
    change_time = Column(TIMESTAMP, nullable=False, server_default=func.now())

class FineLog(Base):
    __tablename__ = 'fine_logs'
    __table_args__ = (
        {'schema': 'db_logs'},
    )
    fine_log_id = Column(Integer, primary_key=True)
    fine_id = Column(Integer, nullable=False)
    table_field = Column(String, nullable=False)
    operation_type = Column(String, nullable=False)
    prev_value = Column(String, nullable=False)
    new_value = Column(String, nullable=False)
    change_time = Column(TIMESTAMP, nullable=False, server_default=func.now())

class OverallLog(Base):
    __tablename__ = 'overall_logs'
    __table_args__ = (
        {'schema': 'db_logs'},
    )
    overall_log_id = Column(Integer, primary_key=True)
    table_name = Column(String, nullable=False)
    table_field = Column(String, nullable=False)
    operation_type = Column(String, nullable=False)
    prev_value = Column(String, nullable=False)
    new_value = Column(String, nullable=False)
    change_time = Column(TIMESTAMP, nullable=False, server_default=func.now())

class Employee(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        CheckConstraint('length(employee_lname) <= 100'),
        CheckConstraint('length(employee_fname) <= 100'),
        CheckConstraint('length(employee_mname) <= 100'),
        CheckConstraint('employee_passport_series BETWEEN 1000 AND 9999'),
        CheckConstraint('employee_passport_number BETWEEN 100000 AND 999999'),
        {'schema': 'employee_schema'},
    )
    employee_id = Column(Integer, primary_key=True)
    employee_lname = Column(String(100), nullable=False)
    employee_fname = Column(String(100), nullable=False)
    employee_mname = Column(String(100))
    employee_passport_series = Column(Integer, nullable=False)
    employee_passport_number = Column(Integer, nullable=False)

class EmployeeCredential(Base):
    __tablename__ = 'employee_credentials'
    __table_args__ = (
        UniqueConstraint('username'),
        CheckConstraint('length(username) <= 100'),
        CheckConstraint('length(password) > 8'),
        {'schema': 'employee_schema'},
    )
    credential_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee_schema.employees.employee_id'), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

    employee = relationship('Employee', back_populates='employee_credentials')

Employee.employee_credentials = relationship('EmployeeCredential', order_by=EmployeeCredential.credential_id, back_populates='employee')