#!/usr/bin/python
import requests
import requests_cache
requests_cache.install_cache(expire_after=30) #not to crash the york 
from bs4 import BeautifulSoup
import copy

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

def get_wosid_and_number():
	pass

def extract_subject_code():
	pass

#pre: takes in a soup object of the subject listing html page.
#post: returns an array of all the subjects, and their respective post urls and post data in a dictionary.
def stage_1_get_all_subjects(subject_listing_soup):
	subject_field = {	
		'subject_name': '',
		'subject_number': '',
		'post_url': '',
		'subject_code': '',
		'subject_data_payload': ''
	}

	all_fields = []

	subject_opts = subject_listing_soup.find("select", { "name" : "subjectPopUp" }).find_all("option")
	payload_number = subject_listing_soup.find("input", {"type" : "submit", "value" : "Search Courses"})["name"]
	wosid= subject_listing_soup.find("input", {"type" : "hidden", "name" : "wosid"})["value"]
	post_url = subject_listing_soup.find("form", { "name" : "subjectForm"} )["action"]


	#populate the array with filled out subject_field dictionaries. 
	for subject in subject_opts:
		current_subject_field = copy.deepcopy(subject_field)
		current_subject_field['subject_name'] = subject.text
		current_subject_field['subject_number'] = subject['value']
		current_subject_field['subject_data_payload']="sessionPopUp=0&subjectPopUp="+current_subject_field['subject_number']+"&"+payload_number+"=Search+Courses&wosid="+wosid
		current_subject_field['post_url'] = post_url
		all_fields.append(current_subject_field)
	
	return all_fields

#pre: takes in a soup object of a subjects course listing html page.
#post: returns an array of all the courses for that subject, and their respective links, code, and name in a dictionary.
def stage_2_get_courses_for_subject(course_listing_soup):
	#TODO: extract faculty, course code, and credit number from course_code...
	class_field = {
		'course_code': '',
		'course_name': '',
		'course_link': '',
	}

	all_classes = []

	courses_found = []
	for i in course_listing_soup.findAll('tr', { "bgcolor":"#ffffff" }):
		courses_found.append(i)

	for i in course_listing_soup.findAll('tr', { "bgcolor":"#e6e6e6" }):
		courses_found.append(i)

	for course in courses_found:
		current_course_field = copy.deepcopy(class_field)
		current_course_field['course_code'] = course.findAll('td')[0].get_text()
		current_course_field['course_name'] = course.findAll('td')[1].get_text()
		current_course_field['course_link'] = "https://w2prod.sis.yorku.ca" + course.select('td a')[0].attrs['href']
		all_classes.append(current_course_field)

	return all_classes

#pre: takes in a soup object of a courses section listing html page.
#post: returns an array of all the sections for that subject, and their respective catagories, and such in a dictionary
def stage_3_get_sections_from_course(section_listing_soup):
	section_field = {
		'description': '',
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

	description = section_listing_soup.select('html body table')[2].select('p')[3].text
	
	print description
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

	if 'You have exceeded the maximum time limit' in subject_soup.get_text():
		print "invalid request credentials."
		quit()

	if "We are currently experiencing technical problems." in subject_soup.get_text():
		print "YorkU server apperantly down..."
		quit()

	
	if (False):
		#this will run all the stages, for all the subjects, for all the courses (not good for testing).
		for subject in stage_1_get_all_subjects(subject_soup):
			course_listing_html = requests.post(subject['post_url'], headers={}, data=subject['subject_data_payload'])
			course_listing_soup = BeautifulSoup(course_listing_html.text.encode('utf-8'))

			stage_2_get_courses_for_subject(course_listing_soup)
	else:
		the_subject = stage_1_get_all_subjects(subject_soup)[0]

		course_listing_html = requests.post(the_subject['post_url'], headers={}, data=the_subject['subject_data_payload'])
		course_listing_soup = BeautifulSoup(course_listing_html.text.encode('utf-8'))

		the_course = stage_2_get_courses_for_subject(course_listing_soup)[0]

		section_listing_html = requests.get(the_course['course_link'])
		section_listing_soup = BeautifulSoup(section_listing_html.text.encode('utf-8'))

		print stage_3_get_sections_from_course(section_listing_soup)
		
if __name__ == "__main__":
   main();