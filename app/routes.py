from flask import Flask, render_template, request, redirect, flash, url_for
from app import app
from datetime import datetime
from dateutil.relativedelta import relativedelta


@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("input_page.html")


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        try:
            rent_pm = request.form["rent_pm"]
            rent_pm = int(rent_pm)
            rate_increase = request.form["rate_increase"]
            rate_increase = int(rate_increase)
            start_date = request.form["start_date"]
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = request.form["end_date"]
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            if start_date > end_date:
                flash("Starting Date cannot be greater than End Date")
                return redirect(url_for("index"))
        except:
            flash("Something Went Wrong")
            return redirect(url_for("index"))

    else:
        flash("Success")
        return redirect(url_for("index"))
    print(rent_pm)
    print(rate_increase)
    print(start_date)
    print(end_date)
    flash("Success")
    return redirect(url_for("index"))
