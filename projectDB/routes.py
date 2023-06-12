from flask import Flask, render_template, request, flash, redirect, url_for, abort
from projectDB import app, db 

@app.route("/")
def index():
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT count(id_school) FROM Schools")
        number_schools=list(cur.fetchone())
        cur.execute("SELECT count(ISBN) FROM Books")
        number_books=list(cur.fetchone())
        cur.close()
        return render_template("landing.html",
                               number_schools = number_schools[0],
                               number_books = number_books[0])
    except Exception as e:
        print(e)
        return render_template("landing.html")


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("errors/404.html", pageTitle = "Not Found"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html", pageTitle = "Internal Server Error"), 500