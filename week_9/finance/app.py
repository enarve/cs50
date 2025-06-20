import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    if request.method == "POST":
        cash = float(request.form.get("cash"))
        if not cash:
            return apology("Can not add empty value")
        if cash <= 0:
            return apology("Amount must be positive")

        old_cash = db.execute("SELECT cash FROM users WHERE id = ?;", user_id)[0].get("cash")
        db.execute("UPDATE users SET cash = ? WHERE id = ?;", old_cash + cash, user_id)
        return redirect("/")

    else:
        user_id = session["user_id"]
        userinfo = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]
        db.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, symbol TEXT NOT NULL, shares INTEGER NOT NULL, price NUMERIC NOT NULL, timestamp TEXT DEFAULT CURRENT_TIMESTAMP);")
        stocks = db.execute(
            "SELECT DISTINCT symbol, SUM(shares) AS shares FROM transactions WHERE (user_id) = (?) GROUP BY symbol;", user_id)
        print(stocks)
        value = 0
        for stock in stocks:
            symbol = stock.get("symbol")
            shares = stock.get("shares")
            price = lookup(symbol).get("price")
            value += shares * price
            stock["price"] = price
            stocks = filter(lambda x: x.get("shares") > 0, stocks)
        return render_template("index.html", userinfo=userinfo, stocks=stocks, value=value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("No symbol provided")
        info = lookup(symbol)
        if not info:
            return apology("Symbol not found")
        try:
            shares = float(request.form.get("shares"))
        except:
            return apology("Shares is not a number")
        if int(shares) != shares or shares < 1:
            return apology("You can buy only positive integer amount of shares")
        shares = int(shares)
        price = info.get("price")
        user_id = session.get("user_id")
        cash = db.execute("SELECT cash FROM users WHERE id = ?;", user_id)[0].get("cash")
        total = price * shares

        if cash >= price:
            db.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, symbol TEXT NOT NULL, shares INTEGER NOT NULL, price NUMERIC NOT NULL, timestamp TEXT DEFAULT CURRENT_TIMESTAMP);")
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?);",
                       user_id, symbol, shares, price)
            db.execute("UPDATE users SET cash = ? WHERE id = ?;", cash - total, user_id)
        else:
            return apology("Not enough money to buy :(")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]
    userinfo = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]
    db.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, symbol TEXT NOT NULL, shares INTEGER NOT NULL, price NUMERIC NOT NULL, timestamp TEXT DEFAULT CURRENT_TIMESTAMP);")
    transactions = db.execute(
        "SELECT DISTINCT symbol, shares, price, timestamp FROM transactions WHERE (user_id) = (?) ORDER BY timestamp;", user_id)
    for trn in transactions:
        symbol = trn.get("symbol")
        shares = trn.get("shares")
        if shares > 0:
            trn["operation"] = "buy"
        else:
            trn["operation"] = "sell"
            trn["shares"] *= -1
    return render_template("history.html", userinfo=userinfo, transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("No symbol provided")
        info = lookup(symbol)
        if info:
            return render_template("quoted.html", info=info)
        else:
            return apology("Symbol not found")
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Username is empty")
        if not password:
            return apology("Provide password")
        if not confirmation:
            return apology("Confirm password")

        if password != confirmation:
            return apology("Password not confirmed")

        users = db.execute("SELECT id, username FROM users WHERE username = ?;", username)
        if users:
            return apology(f"Username {username} already exists")

        hash = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", username, hash)

        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    symbols = db.execute("SELECT DISTINCT symbol FROM transactions WHERE (user_id) = (?);", user_id)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("No symbol provided to sell")
        s = list(map(lambda x: x.get("symbol"), symbols))
        if symbol not in s:
            return apology("No such symbol in your portfolio")
        try:
            shares = float(request.form.get("shares"))
        except:
            return apology("Shares is not a number")
        if int(shares) != shares or shares < 1:
            return apology("You can sell only positive integer amount of shares")
        existing_shares = db.execute(
            "SELECT SUM(shares) as shares FROM transactions WHERE (user_id, symbol) = (?, ?) GROUP BY symbol;", user_id, symbol)[0].get("shares")
        if shares > existing_shares:
            return apology("Not enough shares in portfolio")

        price = lookup(symbol).get("price")
        total = shares * price
        shares_to_sell = (-1) * shares
        db.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, symbol TEXT NOT NULL, shares INTEGER NOT NULL, price NUMERIC NOT NULL, timestamp TEXT DEFAULT CURRENT_TIMESTAMP);")
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?);",
                   user_id, symbol, shares_to_sell, price)
        cash = db.execute("SELECT cash FROM users WHERE id = ?;", user_id)[0].get("cash")
        db.execute("UPDATE users SET cash = ? WHERE id = ?;", cash + total, user_id)

        return redirect("/")
    else:
        return render_template("sell.html", symbols=symbols)
