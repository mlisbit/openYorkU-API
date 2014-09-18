#!/usr/bin/python
import requests
from bs4 import BeautifulSoup

#print html_doc
#print(soup.prettify())

templates = {
	'instructor': {
		'name': '',
		'courses': [],
		'website': ''
	},
	'course': {
		'course_code': '',	
		'course_number': '',
		'course_subject': '',
		'title': '',
		'faculty': '',
		'year_level': 0,
		'credit_count': '',
		'term_years_offered': [],
		'instructors': [],
		'catagories': [],
		'description': '',
		'exclusions': ''
	},
	'catagory': {
		'catagory_code': '',
		'type': 'LECT',
		'day': '',
		'start_time': '',
		'end_time': '',
		'duration': '',
		'location': '',
		'instructor': '',
		'section': '',
		'term': 'F',
		'is_available': False,
		'term_year': '1415'
	}
}

def parse_listing_tables(the_html):
	returning={
		'term': '',
		'section': ''
	}
	print the_html
	first_listing = 2
	listing_increase = 2
	section_html = the_html.select('table tr')[2]
	returning['term'] = the_html.select('font b')[0].get_text().replace('Term', '').strip()
	returning['section'] = the_html.select('font')[0].get_text().replace(the_html.select('font b')[0].get_text(), '').replace('Section', '').strip()
	returning['type'] = section_html.findAll('td', {'valign': 'TOP'})[0].get_text()
	returning['day'] = section_html.findAll('td', {'valign': 'TOP'})[2].get_text()
	returning['start_time'] = section_html.findAll('td', {'valign': 'TOP'})[3].get_text()
	returning['duration'] = section_html.findAll('td', {'valign': 'TOP'})[4].get_text()
	returning['room_number'] = section_html.findAll('td', {'valign': 'TOP'})[5].get_text()
	returning['instructor'] = section_html.findAll('td', {'valign': 'TOP'})[7].get_text()
	print section_html.prettify() #section_html.prettify().encode('utf-8')

#takes in the url of a course.
def get_info(url):
	possible = {
		'description': '',
	}
	course_html = requests.get('https://w2prod.sis.yorku.ca'+url).text
	course_soup = BeautifulSoup(course_html)

	possible['description'] = course_soup.select('html body table')[2].select('p')[3].text

	#for i in course_soup.findAll('')
	
	section_lists = course_soup.select('html body table')[4].select('table')[5]

	course_tables = section_lists.findAll('table')

	'''
	for i in course_tables:
		print i
	'''
	first_listing = 0
	listing_increase = 5
	parse_listing_tables(course_tables[0])
	#print section_lists.findAll('table')[0]


def main():
	wosid="bGAAyTQ96wEggrqeQZq0VM"
	payload_number="1.10.7.5"
	post_url_number="2.1.10.7"
	course_number="0"
	post_number="7"
	payload2="sessionPopUp=0&subjectPopUp="+course_number+"&"+payload_number+"=Search+Courses&wosid="+wosid
	headering={}

	possible_url_2 = "https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm.woa/"+post_number+"/wo/"+wosid+"/"+post_url_number
	r = requests.post(possible_url_2, headers=headering, data=payload2)

	html_doc = r.text.encode('utf-8')

	soup = BeautifulSoup(html_doc)

	if 'You have exceeded the maximum time limit' in soup.get_text():
		print "invalid request credentials."
		quit()

	if "We are currently experiencing technical problems." in soup.get_text():
		print "YorkU server apperantly down..."
		quit()

	
	courses_found = []
	for i in soup.findAll('tr', { "bgcolor":"#ffffff" }):
		courses_found.append(i)

	for i in soup.findAll('tr', { "bgcolor":"#e6e6e6" }):
		courses_found.append(i)

	#print soup.get_text()
	get_info(courses_found[0].select('td a')[0].attrs['href'])

					
if __name__ == "__main__":
   main();




#soup.findAll('a', { "class":"hdrlnk" }
