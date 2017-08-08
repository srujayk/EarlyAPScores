from flask import Flask, flash, redirect, render_template, request, session, url_for
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import lxml

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

		#connects to collegeboard.org
		browser = RoboBrowser()
		login_url = 'https://account.collegeboard.org/login/login?appId=287&DURL=https://apscore.collegeboard.org/scores/view-your-scores'
		browser.open(login_url)

		#logs in to collegeboard.org with user credentials
		form = browser.get_form(id='loginForm')
		form['person.userName'].value = request.form.get("username")
		form['person.password'].value = request.form.get("password")
		form.serialize()
		browser.submit_form(form)

		#redirects to AP scores page on collegeboard.org
		browser.open('https://apscore.collegeboard.org/scores/view-your-scores')

		#populates exams_final with exam names scraped from collegeboard.org
		exams = browser.select(".span5 > h4")
		exams_final = []
		for exam in exams:
			exam = str(exam)
			exams_final.append(exam[4:-5])

		#populates scores_final with scores scraped from collegeboard.org
		scores = browser.select(".span5 > span > em")
		scores_final = []
		for score in scores:
			score = str(score)
			scores_final.append(score[4:-5])

		#returns scores page
		return render_template("scored.html", exams=exams_final, scores=scores_final)  

if __name__ == '__main__':
    #app.debug = True
    app.run()
    
        
