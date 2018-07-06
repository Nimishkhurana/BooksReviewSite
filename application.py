from flask import Flask,render_template,request,session,redirect,url_for,jsonify
from flask_session import Session
import os
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


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
    search_by = request.form.get("search_by")
    search_book = request.form.get("search_book")
    ## Searching matching books
    books = db.execute(f'SELECT * FROM books WHERE {search_by} LIKE :search_book',{"search_book":f"%{search_book}%"}).fetchall()
    rows = db.execute(f'SELECT * FROM books WHERE {search_by} LIKE :search_book',{"search_book":f"%{search_book}%"}).rowcount

    if rows == 0:
        return jsonify({"success":False,"error":"No book found"})

    for book in books:
        titles.append(book["title"])
        authors.append(book["author"])
    return jsonify({"success":True,"titles":titles,"authors":authors})












    # res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "sm2j54RqyCDvbeHG2QBtw", "isbns": })
    # print(res.json())
