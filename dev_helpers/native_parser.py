#!/usr/bin/python
import requests
import requests_cache
requests_cache.install_cache(expire_after=30) #not to crash the york 
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
#THIS SHOULD BE REMOVED, and replaced with a proper stage parser...
'''
def get_info(url):
	possible = {
		'description': '',
	}
	course_html = requests.get('https://w2prod.sis.yorku.ca'+url).text
	course_soup = BeautifulSoup(course_html)

	possible['description'] = course_soup.select('html body table')[2].select('p')[3].text

	#for i in course_soup.findAll('')
	
	#section_lists = course_soup.select('html body table')[4].select('table')[5]
	
	section_lists = course_soup.select('html body table table table')[-1]
	print section_lists

	parse_listing_tables(section_lists)
	
	
	#course_tables = section_lists.findAll('table')


	#for i in course_tables:
	#	print i

	first_listing = 0
	listing_increase = 5
	#parse_listing_tables(course_tables[0])
	#print section_lists.findAll('table')
'''

def stage_1_get_all_subjects(course_listing_soup):
	#should get a list of the subjects, store them in a dictionary, return it.
	subject_field = {
		'subject_name': '',
		'subject_number': '',
		'request_url': ''
	}

	courses_found = []
	for i in course_listing_soup.findAll('tr', { "bgcolor":"#ffffff" }):
		courses_found.append(i)

	for i in course_listing_soup.findAll('tr', { "bgcolor":"#e6e6e6" }):
		courses_found.append(i)

	all_fields = []
	return all_fields

def stage_2_get_courses_for_subject(subjects):
	#wall the courses withing a certain subject. The table contains a field that shows a link to the couse Schedule (this will be stage 3)
	class_field = {
		'course_code':'',
		'course_code':'',
		'course_link': '',
		'request_url': ''
	}
	all_classes = []

	return all_classes

def stage_3_get_sections_from_course(courses):
	#get information for all the sections for a given course
	section_field = {
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
	all_sections = []
	return all_sections


def main():
		
	base_url = "https://w2prod.sis.yorku.ca"

	#Start from root of the webobject application to generate proper session tokens
	cdm_home = requests.get(base_url + "/Apps/WebObjects/cdm.woa")
	cdm_soup = BeautifulSoup(cdm_home.text.encode('utf-8'))

	search_url = cdm_soup.find('a',  text="Subject")['href']
	subject_select = requests.get(base_url + search_url)

	subject_soup = BeautifulSoup(subject_select.text.encode('utf-8'))
	subject_opts = subject_soup.find("select", { "name" : "subjectPopUp" }).find_all("option")
	
	subject_hash = {}
	for subject in subject_opts:
		subject_hash[subject['value']] = subject.text

	
	post_url = subject_soup.find("form", { "name" : "subjectForm"} )["action"]
	payload_number = subject_soup.find("input", {"type" : "submit", "value" : "Search Courses"})["name"]
	wosid= subject_soup.find("input", {"type" : "hidden", "name" : "wosid"})["value"]

	
	course_number = subject_hash.keys()[0]

	payload2="sessionPopUp=0&subjectPopUp="+course_number+"&"+payload_number+"=Search+Courses&wosid="+wosid
	headering={}

	
	r = requests.post(post_url, headers=headering, data=payload2)

	html_doc = r.text.encode('utf-8')

	soup = BeautifulSoup(html_doc)

	if 'You have exceeded the maximum time limit' in soup.get_text():
		print "invalid request credentials."
		quit()

	if "We are currently experiencing technical problems." in soup.get_text():
		print "YorkU server apperantly down..."
		quit()

	print stage_1_get_all_subjects(soup);

					
if __name__ == "__main__":
   main();