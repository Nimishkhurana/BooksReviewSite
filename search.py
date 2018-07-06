import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_UR"))
db = scoped_session(sessionmaker(bind=engine))

search_by = "author"
search_book = "Terry"
def main():

    books = db.execute(f'SELECT * FROM books WHERE {search_by} LIKE :search_book',{"search_book":f"%{search_book}%"}).fetchall()

    for book in books:
        print(book["isbn"])


if __name__ == '__main__':
    main()
