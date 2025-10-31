import sqlite3
from flask import Flask, render_template, redirect, url_for, request, abort, session

# ------------------------
# Flask App Configuration
# ------------------------
app = Flask(__name__)
print(">>> LOADED main.py FROM:", __file__)
app.config["SECRET_KEY"] = "dev"  # needed for extra credit (sessions)

@app.before_request
def require_login_for_protected_pages():
    # pages that do NOT need login
    open_endpoints = {"login", "static"}
    # allow the error handler during 404 etc.
    if request.endpoint in open_endpoints:
        return
    # if not logged in, go to /login
    if not session.get("logged_in"):
        return redirect(url_for("login"))

# ------------------------
# Database Setup
# ------------------------
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          content TEXT NOT NULL,
          created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

# ------------------------
# Helper: Get a single post
# ------------------------
def get_post(id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

# ------------------------
# ROUTES
# ------------------------

@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts ORDER BY created DESC").fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route("/<int:id>")
def post(id):
    p = get_post(id)
    return render_template("post.html", post=p)

@app.route("/<int:id>/edit", methods=("GET", "POST"))
def edit(id):
    p = get_post(id)
    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"].strip()
        conn = get_db_connection()
        conn.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for("post", id=id))
    return render_template("edit.html", post=p)

@app.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"].strip()
        if title and content:
            conn = get_db_connection()
            conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for("index"))
    return render_template("create.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        u = request.form.get("username", "")
        p = request.form.get("password", "")
        if u == "admin" and p == "admin":
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            error = "Invalid Credentials. Please try again."
    return render_template("login.html", error=error)
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")
