#!/usr/bin/python
import requests
import requests_cache
requests_cache.install_cache(expire_after=30) #not to crash the york 
from bs4 import BeautifulSoup
import copy
import time
import json
from datetime import datetime, timedelta

##########################################################################################
##########################################################################################
##																						##
## For any one reading this code, and wondering why parsing looks so horrible:   		##
## Part of it's because beautifulsoup4 cannot properly parse York Universities site..	##
##																						##
##########################################################################################
##########################################################################################

# pre: takes in the text from a soup object
# post: return true if the page returned a valid response. quit the program gracefully, and output details about what
# program last parsed. 
def check_if_not_kicked(soup_text):
	if 'You have exceeded the maximum time limit' in soup_text.get_text():
		f = open('progress', 'w')
		f.write('FAULT: \'invalid request credentials.\'\n')
		f.close()
		print "invalid request credentials."
		quit()

	if "We are currently experiencing technical problems." in soup_text.get_text():
		f = open('progress', 'w')
		f.write('FAULT: \'We are currently experiencing technical problems\'\n')
		f.close()
		print "YorkU server apperantly down..."
		quit()

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

	check_if_not_kicked(course_listing_soup)

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
		'catagory_number': '',
		'type': '',
		'day': '',
		'start_time': '',
		'end_time': '',
		'duration': '',
		'location': '',
		'instructor': '',
		'section': '',
		'term': '',
		'term_year': '1415',
		'notes': '',
		'building':  ''
	}

	description = section_listing_soup.select('html body table')[2].select('p')[3].text
	#get the soup for all the mini tables (includes some junk)
	tables = section_listing_soup.select('body')[0].findAll('td', {'colspan': '3'})
	important_table = []

	#getting the section and term letters, placing them in order into an array
	section_letters = []
	term_letters = []
	for i in section_listing_soup.select('body')[0].findAll('td', {'bgcolor': '#CC0000'}):
		#get the text from the red table heading, and extract the term letter, and section letter.
		red_table_heading = filter(bool, i.get_text().strip().split(' '))
		section_letters.append(red_table_heading[3])
		term_letters.append(red_table_heading[1])


	#removes the junk from the previous scrape. 
	for i in range(1, len(tables), 2):
		important_table.append(tables[i])

	#get all the important fields.
	all_sections = []
	for term_and_section_counter, table in enumerate(important_table):
		
		# this combines the top row of the table with the rows of the table following it,
		# dont remember why I do this... 
		result_table_text = []
		result_table_text.append(table.findAll('td', {'valign': 'TOP'})[0].parent.get_text('|').encode('utf-8'))
		for sub_table in range(0, len(table.findAll('td', {'valign': 'TOP'})[0].parent.find_next_siblings())):
			result_table_text.append(table.findAll('td', {'valign': 'TOP'})[0].parent.find_next_siblings()[sub_table].get_text('|').encode('utf-8'))
		
	
		for row in result_table_text:
			#print row
			split_row = row.split('|')
			current_section_field = copy.deepcopy(section_field)
			current_section_field['term'] = term_letters[term_and_section_counter]
			current_section_field['section'] = section_letters[term_and_section_counter]
			current_section_field['description'] = description
			current_section_field['type'] = ''.join([i for i in split_row[0] if not i.isdigit()])
			current_section_field['day'] = split_row[1].strip()
			current_section_field['start_time'] = split_row[2].strip()
			current_section_field['duration'] = split_row[3].strip()
			current_section_field['location'] = split_row[4].strip()
			
			
			try:
				#this course must be canceled if this exception is hit.
				current_section_field['catagory_number'] = split_row[5].strip()
				current_section_field['instructor'] = split_row[6].strip()
				if split_row[2].strip() == 'Cancelled':
					pass
			except:
				current_section_field['catagory_number'] = 'N/A'
				current_section_field['instructor'] = 'N/A'

			try:
				#this will fail when it's an online course, or if the course is canceled. 
				#They do not have course codes, nor start times and end times. 
				#example: FILM 1701
				current_section_field['end_time'] = (datetime.strptime(current_section_field['start_time'], "%H:%M") + timedelta(minutes=int(float(current_section_field['duration'])))).strftime("%H:%M")
				current_section_field['notes'] = split_row[7].strip()
			except:
				current_section_field['notes'] = ''
				current_section_field['end_time'] = 'N/A'

			current_section_field['building'] = ''.join([i for i in current_section_field['location'] if not i.isdigit()])
			all_sections.append(copy.deepcopy(current_section_field))

	return all_sections

def main():
	base_url = "https://w2prod.sis.yorku.ca"

	#Start from root of the webobject application to generate proper session tokens
	cdm_home = requests.get(base_url + "/Apps/WebObjects/cdm.woa")
	cdm_soup = BeautifulSoup(cdm_home.text.encode('utf-8'))

	search_url = cdm_soup.find('a',  text="Subject")['href']
	subject_select = requests.get(base_url + search_url)
	print "session and request url: " + str(base_url + search_url)

	subject_soup = BeautifulSoup(subject_select.text.encode('utf-8'))
	subject_count = len(stage_1_get_all_subjects(subject_soup)) - 1 #count all the subjects.

	time.sleep(30) #if there's no delay, yorku wont serve the request.

	if (True):
		#sigh, we have to regenerate a new session key on every request for a new subject, otherwise york may drop the request.
		for current_subject_index in range(0, subject_count):
			base_url = "https://w2prod.sis.yorku.ca"

			#Start from root of the webobject application to generate proper session tokens
			cdm_home = requests.get(base_url + "/Apps/WebObjects/cdm.woa")
			cdm_soup = BeautifulSoup(cdm_home.text.encode('utf-8'))

			search_url = cdm_soup.find('a',  text="Subject")['href']
			subject_select = requests.get(base_url + search_url)
			print "session and request url: " + str(base_url + search_url)
			
			subject_soup = BeautifulSoup(subject_select.text.encode('utf-8'))

			current_subject = stage_1_get_all_subjects(subject_soup)[current_subject_index]

			course_listing_html = requests.post(current_subject['post_url'], headers={}, data=current_subject['subject_data_payload'])
			course_listing_soup = BeautifulSoup(course_listing_html.text.encode('utf-8'))

			all_courses = stage_2_get_courses_for_subject(course_listing_soup)
			#print all_courses[3]
			for course in all_courses:
				print  json.loads(json.dumps(course['course_code'], ensure_ascii=False, indent=4))
				section_listing_html = requests.get(course['course_link'])
				section_listing_soup = BeautifulSoup(section_listing_html.text.encode('utf-8'))

				listings = stage_3_get_sections_from_course(section_listing_soup)
				for i in listings:
					#print i
					pass

			time.sleep(30) #if there's no delay, yorku wont serve the request.

	else:
		the_subject = stage_1_get_all_subjects(subject_soup)[0]
		
		course_listing_html = requests.post(the_subject['post_url'], headers={}, data=the_subject['subject_data_payload'])
		course_listing_soup = BeautifulSoup(course_listing_html.text.encode('utf-8'))

		#for i in range(0, stage_2_get_courses_for_subject(course_listing_soup).__len__()):
		#	print i, stage_2_get_courses_for_subject(course_listing_soup)[i]['course_code']
		the_course = stage_2_get_courses_for_subject(course_listing_soup)[0]
		print  json.loads(json.dumps(the_course['course_code'], ensure_ascii=False, indent=4))
		#print the_course['course_code']

		section_listing_html = requests.get(the_course['course_link'])
		section_listing_soup = BeautifulSoup(section_listing_html.text.encode('utf-8'))

		sections = stage_3_get_sections_from_course(section_listing_soup)
		for i in sections:
			print i
		
if __name__ == "__main__":
   main();