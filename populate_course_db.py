#!ve/bin/python
import requests
import json

if __name__ == '__main__':
	data2 = {
		'course_code': 'test',
		'subject_abv': '',
		'subject_full': '',
		'faculty': '',
		'year': 0,
		'credits': '',
		'title': '',
		'description': '',
	}
	r = requests.post('http://127.0.0.1:5000/courses/', data=json.dumps(data2))
	print r
	'''
	with open('course_list.txt', 'rU') as f:
		for line in f:	
			pass
	'''