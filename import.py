import os
import csv
from itertools import islice
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    file = open("books.csv")
    data = csv.reader(file)
    count = 0
    for isbn,title,author,year in islice(data,2579,None):
        try:
            db.execute("INSERT INTO books (isbn,title,author,year) VALUES (:isbn,:title,:author,:year)",{"isbn":isbn,"title":title,"author":author,"year":int(year)})
            print(f"Added book title: {title}")
            count +=1
            db.commit()
        except:
            continue

    print("No of books",count)


if __name__ == '__main__':
    main()
