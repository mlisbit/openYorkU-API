#!ve/bin/python
import requests
import json

if __name__ == '__main__':
	course_data_template = {
		'course_code': 'test',
		'course_subject': '',
		'title': '',
		'faculty': '',
		'study_year': 0,
		'credit_count': '',
		'instructors': [],
		'description': '',
		'term_year': 0,
	}
	r = requests.post('http://127.0.0.1:5000/courses/', data=json.dumps(course_data_template))
	print r
	'''
	with open('course_list.txt', 'rU') as f:
		for line in f:	
			pass
	'''