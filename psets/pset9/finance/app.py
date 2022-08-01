from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session["user_id"]
    stocks = db.execute("SELECT symbol, name, price, SUM(shares) as totalShares FROM transactions WHERE user_id=:user_id GROUP BY symbol",
                        user_id=user_id)
    cash = db.execute("SELECT cash FROM users WHERE id=:id", id=user_id)[0]["cash"]
    total = cash

    for stock in stocks:
        total += stock["price"] * stock["totalShares"]

    return render_template("index.html", stocks=stocks, cash=cash, usd=usd, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        user_id = session["user_id"]

        # Retorna un apology si no ingresa un simbolo adecuado
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        # Retorna un apology si no ingresa el precio
        elif not request.form.get("shares"):
            return apology("must provide shares", 400)
        # Retorna apology si no es un numero
        elif not request.form.get("shares").isnumeric():
            return apology("must provide a number", 400)
        # Retorna apology si es menor que 1
        elif int(request.form.get("shares")) < 1:
            return apology("must provide an positive number", 400)

        quote = lookup(symbol)
        # Verifica si el simbolo ingresado es el adecuado
        if not quote:
            return apology("symbol not found", 400)

        price = quote["price"]
        total = int(shares) * price
        name = quote["name"]

        cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

        if total > float(cash[0]["cash"]):
            return apology("don't have enough cash")

        db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (:user_id, :name, :shares, :price, :type, :symbol)",
                   user_id=user_id, name=name, shares=shares, price=price, type='buy', symbol=symbol)

        db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=cash[0]["cash"]-total, id=session["user_id"])

        flash("Bougth")

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    query = db.execute("SELECT type, symbol, price, shares, time FROM transactions")

    return render_template("history.html", query=query)


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
        rows = db.execute("SELECT * FROM users WHERE username=:username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
        stock = lookup(request.form.get("symbol"))
        # Se le pasa el simbolo a quote
        if not stock:
            return apology("symbol not found", 400)

        # Válida si se ha ingresado un valor
        if not request.form.get("symbol"):
            return apology("provide a stock name", 400)

        return render_template("quoted.html", symbol=stock["symbol"], price=stock["price"])

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Se llama la funcion para olvidar cualquier id de usuario
    session.clear()

    if request.method == "POST":

        # Válida si se pasa el nombre de usuario

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("test", 400)

        if password != confirmation:
            return apology("password don't match", 400)

        user = db.execute("SELECT * FROM users WHERE username=:username", username=username)
        # Si ya existe retorna un error
        if len(user) == 1:
            return apology("Username already exists", 400)

        # Inserta el usuario y la contraseña a sus respectivas columnas
        insert = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        if not insert:
            return apology("username not validate", 200)

        session["user_id"] = insert

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    symbol = request.form.get("symbol")
    shares = request.form.get("shares")

    if request.method == "POST":
        if int(shares) <= 0:
            return apology("provide valid number")

        quote = lookup(symbol)

        if not quote:
            return apology("symbol not exist")
        price = quote["price"]
        name = quote["name"]
        total = price * int(shares)

        query = db.execute("SELECT shares FROM transactions WHERE user_id=:id AND symbol =:symbol GROUP BY symbol",
                           id=session["user_id"], symbol=symbol)[0]["shares"]

        if query < int(shares):
            return apology("can't sell more shares than you have")

        cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])[0]["cash"]
        db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=cash, id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (:user_id, :name, :shares, :price, :type, :symbol)",
                   user_id=session["user_id"], name=name, shares=-int(shares), price=+total, type='sell', symbol=symbol)

        return redirect("/")

    else:
        user_id = session["user_id"]
        symbols = db.execute("SELECT symbol FROM transactions WHERE user_id=:id GROUP BY symbol", id=user_id)

        return render_template("sell.html", symbols=symbols)


@app.route("/changePassword", methods=["GET", "POST"])
def changePassword():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Válida si se pasa el nombre de usuario

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not password or not confirmation:
            return apology("provide passwords", 400)

        if password != confirmation:
            return apology("passwords don't match", 400)

        update = db.execute("UPDATE users SET hash=:hash", hash=generate_password_hash(request.form.get("password")))

        return redirect("/")

    else:
        return render_template("changePassword.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
