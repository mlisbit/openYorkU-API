#!ve/bin/python
import requests
import json
import copy

term_offered_template = {'term_year': 0, 'terms': []}
course_data_template = {
	'course_code': '',	
	'course_number': '',
	'course_subject': '',
	'title': '',
	'faculty': '',
	'year_level': 0,
	'credit_count': '',
	'terms_offered': [],
	'instructors': [],
	'description': '',
	'term_year': 0,
}

term_year = 1415
term = "W or F"

def populate_course_db():
	result_post = []
	with open('txt_files/course_list.txt', 'rU') as f:
		for line in f:	
			if line.strip():
				new_data = copy.deepcopy(course_data_template)
				new_term_data = copy.deepcopy(term_offered_template)

				sections = line.split('\t')

				first_part = sections[0].split(' ')
				faculty_and_course_code = first_part[0].split('/')

				new_data['title'] = sections[1]
				new_data['faculty'] = faculty_and_course_code[0]
				new_data['course_subject'] = faculty_and_course_code[1]
				new_data['course_number'] = first_part[1]
				new_data['year_level'] = int(new_data['course_number'][0])
				new_data['credit_count'] = int(float(first_part[2]))
				new_data['term_year'] = term_year
				new_data['course_code'] = new_data['course_subject']+new_data['course_number']

				new_term_data['term_year'] = new_data['term_year']
				new_term_data['terms'].append(term)

				new_data['terms_offered'].append(new_term_data)
				result_post.append(new_data)
	return result_post

def populate_subject_db():
	pass

if __name__ == '__main__':
	#print json.dumps(new_data, sort_keys=True, indent=4, separators=(',', ': '))
	for i in populate_course_db():
		r = requests.post('http://127.0.0.1:5000/courses/', data=json.dumps(i))
		