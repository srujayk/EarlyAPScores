from flask import Flask, flash, redirect, render_template, request, session, url_for

from apscores import *

# configure application
app = Flask(__name__)

@app.route("/")
def index():

    #returns home page
	return render_template("index.html")

@app.route("/scores", methods=["GET", "POST"])
def scores():

	if request.method == "GET":

		#return login form
		return render_template("scores.html")

	if request.method == "POST":

		exams_final = get_scores(request.form.get("username"), request.form.get("password"))

		#returns scores page
		return render_template("scored.html", exams=exams_final)

if __name__ == '__main__':
    #app.debug = True
    app.run()
