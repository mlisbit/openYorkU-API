#!ve/bin/python
import requests

if __name__ == '__main__':
	data = {
		'course_code': '',
		'subject_abv': '',
		'subject_full': '',
		'faculty': '',
		'year': 0,
		'credits': '',
		'title': '',
		'description': '',
	}
	requests.post('localhost:5000', data=payload2)
	'''
	with open('course_list.txt', 'rU') as f:
		for line in f:	
			pass
	'''