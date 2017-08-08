from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import lxml
from lxml import html

def main():
	username = input("Enter your CollegeBoard username: ")
	password = input("Enter your CollegeBoard password: ")

	exams_final = get_scores(username, password)
	print()
	for exam in exams_final:
		print("Year: {} ({})".format(exam[0], exam[1]))
		
		for score in exam[2]:
			print(score[0] + ": " + score[1])

		print()

def get_scores(username, password):

	browser = RoboBrowser(parser="lxml")
	login_url = 'https://account.collegeboard.org/login/login?appId=287&DURL=https://apscore.collegeboard.org/scores/view-your-scores'
	browser.open(login_url)

	form = browser.get_form(id='loginForm')
	form['person.userName'].value = username
	form['person.password'].value = password

	form.serialize()
	browser.submit_form(form)

	browser.open('https://apscore.collegeboard.org/scores/view-your-scores')

	exams = browser.select("html")
	tree = html.document_fromstring(str(exams[0]))

	exams_final = []
	exam_years = tree.xpath('//div[@class="year-scores"]/div[@class="headline"]/h3/text()')
	for exam_year in exam_years:
		exams_final.append([str(exam_year)])

	ab_subscore = tree.xpath('//ul[@class="bullet"]/li/em/text()')

	for i in range(len(exam_years)):
		exam_year_awards = tree.xpath('//div[{}][@class="year-scores"]/div[@class="headline"]/div/div/a/@title'.format(str(i + 1)))
		if exam_year_awards == []:
			exams_final[i].append("Award: None")
		else:
			exams_final[i].append(str(exam_year_awards[0]))

		exam_year_names = tree.xpath('//div[{}][@class="year-scores"]/div[@class="year-exams-container"]/div/div/h4/text()'.format(str(i + 1)))
		exam_year_scores = tree.xpath('//div[{}][@class="year-scores"]/div[@class="year-exams-container"]/div/div/span/em/text()'.format(str(i + 1)))

		exams_final[i].append([])
		for j in range(len(exam_year_names)):
			if str(exam_year_names[j]) == 'Calculus BC':
				exams_final[i][2].append([str(exam_year_names[j]), str(exam_year_scores[j]) + " (AB Subscore: {})".format(str(ab_subscore[0]))])
			else:
				exams_final[i][2].append([str(exam_year_names[j]), str(exam_year_scores[j])])

	return(exams_final)

if __name__ == '__main__':
    main()
