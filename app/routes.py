from flask import Flask, render_template, request, redirect, flash, url_for, send_file
from app import app
from datetime import datetime
from dateutil.relativedelta import relativedelta
import tempfile
from calculator.Calculator import calculate_rent
import csv


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
    headers, data = calculate_rent(
        start_date=start_date, end_dates=end_date, rent=rent_pm, rate=rate_increase
    )

    time = datetime.now()
    time = time.strftime("%d-%m-%Y")
    filename = f"data_{time}.csv"
    with tempfile.NamedTemporaryFile(mode="w", newline="", delete=False) as temp_file:
        csvwriter = csv.writer(temp_file)
        # writing the heades rows
        csvwriter.writerow(headers)
        # writing the data rows
        csvwriter.writerows(data)
        temp_file_path = temp_file.name

    flash("Success")
    # return redirect(url_for("index"))
    return send_file(temp_file_path, as_attachment=True, download_name=filename)
