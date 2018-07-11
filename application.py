from flask import Flask,render_template,request,session,redirect,url_for,jsonify,json
from flask_session import Session
import os,decimal
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_UR"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/getstarted",methods=["GET"])
def signpage():
    if 'user_id' not in session:
        return render_template("signup.html")
    else:
        return redirect(url_for("search"))


@app.route("/signup",methods=["POST"])
def signup():
    username = request.form.get("username")
    email = request.form.get("register-email")
    password = request.form.get("signup_password")

    # inserting user data in database

    db.execute("INSERT INTO users (username,email,password) VALUES (:username,:email,:password)",
    {"username":username,"email":email,"password":password})
    db.commit()

    user_id = db.execute("SELECT user_id FROM users WHERE email = :email",{"email":email}).fetchone()
    session["user_id"] = user_id

    return redirect(url_for("search"))

@app.route("/signin",methods=["POST"])
def signin():
    email = request.form["login-email"]
    password = request.form["login-password"]

    user = db.execute("SELECT * FROM users WHERE email = :email AND password = :password",
    {"email":email,"password":password}).fetchone()

    if user is None:
        error = "Invalid Credentials"
        return render_template("signup.html",error=error)

    user_id = user["user_id"]
    session["user_id"] = user_id
    return redirect(url_for("search"))

@app.route("/search")
def search():
    if "user_id" in session:
        username = (db.execute("SELECT * FROM users WHERE user_id = :user_id",{"user_id":session["user_id"]}).fetchone())["username"]
        return render_template("search.html",username = username)

    return redirect(url_for("signpage"))


@app.route("/logout")
def logout():
    session.pop("user_id",None)
    return redirect(url_for("home"))


@app.route("/searching",methods=["POST","GET"])
def searching():
    titles = []
    authors = []
    ids = []
    search_by = request.form.get("search_by")
    search_book = request.form.get("search_book")
    ## Searching matching books
    books = db.execute(f'SELECT * FROM books WHERE {search_by} LIKE :search_book ORDER BY title,author,year',{"search_book":f"%{search_book}%"}).fetchall()
    rows = db.execute(f'SELECT * FROM books WHERE {search_by} LIKE :search_book',{"search_book":f"%{search_book}%"}).rowcount

    if rows == 0:
        return jsonify({"success":False,"message":"No book found"})

    for book in books:
        titles.append(book["title"])
        authors.append(book["author"])
        ids.append(book["id"])
    return jsonify({"success":True,"ids":ids,"titles":titles,"authors":authors,"message":"Matching books:"})

@app.route("/details/<int:book_id>")
def details(book_id):
    # return f"Book id is {book_id}"
    book_data = db.execute("SELECT * FROM books WHERE id = :book_id",{"book_id":book_id}).fetchone()
    book = {"isbn":book_data[1],"title":book_data[2],"author":book_data[3],"year":book_data[4]}

    avg_rating_count = db.execute("SELECT AVG(rating),COUNT(rating) FROM book_reviews WHERE id_book = :book_id",{"book_id":book_id}).fetchone()
    avg,total_count = avg_rating_count[0],avg_rating_count[1]

    if total_count == None:
        total_count = 0




    ratings_count = {}
    ratings = db.execute("SELECT rating,count(rating) FROM book_reviews WHERE id_book = :book_id GROUP BY rating",{"book_id":book_id}).fetchall()

    # ratings_count => stars count
    for a in ratings:
        ratings_count[a[0]] = a[1]
    for i in range(1,6):
        if i not in ratings_count:
            ratings_count[i] = 0


    all_reviews = db.execute("SELECT users.username,book_reviews.rating,book_reviews.date_posted,book_reviews.text_review FROM book_reviews JOIN users ON book_reviews.id_user = users.user_id  WHERE book_reviews.id_book = :book_id",{"book_id":book_id}).fetchall();

    individual_reviews = []

    for review in all_reviews:
        if review[3] != None:
            areview = {}
            areview["username"] = review[0]
            areview["rating"] = review[1]
            areview["date"] = review[2].strftime("%d %b %Y")
            areview["text_review"]  = review[3]
            individual_reviews.append(areview)

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "sm2j54RqyCDvbeHG2QBtw", "isbns": "9781632168146"})

    if res.status_code !=200:
        goodreads = {"success":False,"error":"No reviews found from external sources"}
    else :
        goodreads = {"success":True,"count":(res.json())["books"][0]["work_reviews_count"],"avg_rating":(res.json())["books"][0]["average_rating"]}

    complete_reviews = {"avg":avg,"total_count":total_count,"ratings_count":ratings_count,"individual_reviews":individual_reviews,"goodreads":goodreads}

    return render_template("details.html",book = book,complete_reviews = json.dumps(complete_reviews,default = decimal_default))





# insert into book_reviews (id_book,id_user,rating,text_review) values (1,4,3,"Good book to read .It incresed my knowledge very much.");









    # res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "sm2j54RqyCDvbeHG2QBtw", "isbns": })
    # print(res.json())
