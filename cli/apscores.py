from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import lxml

browser = RoboBrowser()
login_url = 'https://account.collegeboard.org/login/login?appId=287&DURL=https://apscore.collegeboard.org/scores/view-your-scores'
browser.open(login_url)

form = browser.get_form(id='loginForm')
form['person.userName'].value = 'srujayk' 
form['person.password'].value = 'junk'

form.serialize()
browser.submit_form(form)

browser.open('https://apscore.collegeboard.org/scores/view-your-scores')

exams = browser.select(".span5 > h4")

exams_final = []
scores_final = []

for exam in exams:
	exam = str(exam)
	exams_final.append(exam[4:-5])

scores = browser.select(".span5 > span > em")
for score in scores:
	score = str(score)
	scores_final.append(score[4:-5])

for i in range(len(exams)):
	print("Score of AP {}: {}".format(exams_final[i], scores_final[i]))

