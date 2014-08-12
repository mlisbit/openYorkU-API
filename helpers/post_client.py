#!/usr/bin/python
import requests, sys, getopt
import json
import copy

headers = {'content-type': 'application/json'}

course_data_template = {
	'course_code': '',	
	'course_number': '',
	'course_subject': '',
	'title': '',
	'faculty': '',
	'year_level': 0,
	'credit_count': '',
	'term_years_offered': [],
	'instructors': [],
	'description': ''
}

subject_data_template = {
	'code': '',
	'title': ''
}

building_data_template = {
	'name': '',
	'building_code': '',
	'cover_polygon': [
		{
			'lon': 0,
			'lat': 0
		}
	],
	'location': {
		'lon': 0,
		'lat': 0
	},
	'year_built': 0,
	'history': '',
}

restaurant_data_template = {
	'name'		: '',
	'telephone'	: '',
	'building'	: '',
	'tags'		: '',
	'hours' 	: {
		'monday'		: {'open': '', 'close': ''},
		'tuesday'		: {'open': '', 'close': ''},
		'wednesday'		: {'open': '', 'close': ''},
		'thursday'		: {'open': '', 'close': ''},
		'friday'		: {'open': '', 'close': ''},
		'saturday'		: {'open': '', 'close': ''},
		'sunday'		: {'open': '', 'close': ''}
	},
	'logo_url'	: '',
	'serves_booze': ''
}

term_year = 1415
term = "W or F"

def get_course_db():
	result_post = []
	with open('txt_files/course_list.txt', 'rU') as f:
		for line in f:	
			if line.strip():
				new_data = copy.deepcopy(course_data_template)
				
				sections = line.split('\t')

				first_part = sections[0].split(' ')
				faculty_and_course_code = first_part[0].split('/')

				new_data['title'] = sections[1].strip()
				new_data['faculty'] = faculty_and_course_code[0]
				new_data['course_subject'] = faculty_and_course_code[1]
				new_data['course_number'] = first_part[1]
				new_data['year_level'] = int(new_data['course_number'][0])
				new_data['credit_count'] = int(float(first_part[2]))
				new_data['course_code'] = new_data['course_subject']+new_data['course_number']

				new_data['term_years_offered'].append(term_year)
				new_data.pop("instructors", None)
				result_post.append(new_data)
	return result_post

def get_subject_db():
	result_post=[]
	with open('txt_files/subject_list.txt', 'rU') as f:
		for line in f:
			if line.strip():
				new_data = copy.deepcopy(subject_data_template)
				sections = line.split('-')
				
				new_data['code'] = sections[0].strip()
				new_data['title'] = sections[1].strip()
				result_post.append(new_data)
	return result_post

def get_restaurant_db():
	result_post=[]
	section_line = 0
	with open('txt_files/restaurant_list.txt', 'rU') as f:
		for line in f:
			if line.strip():
				line = line.strip()
				if (section_line == 0):
					new_data = copy.deepcopy(restaurant_data_template)
					if '*' in line:
						new_data['serves_booze'] = True
						line = line.replace('*', '')
					new_data['name'] = line.strip()
					section_line += 1
				elif (section_line == 1):
					new_data['building'] = line.split(',')[1].strip()
					section_line += 1
				elif (section_line == 2):
					new_data['telephone'] = line.strip()
					section_line += 1
				elif (section_line == 3):
					#time to parse that hour string.
					days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
					day_data = line.strip().split(',')
					for current,day_hours in enumerate(day_data):
						if (day_hours.strip().upper() != 'CLOSED'):
							new_data['hours'][days[current]]['open'] = day_hours.split('-')[0].strip()
							new_data['hours'][days[current]]['close'] = day_hours.split('-')[1].strip()
						else:
							new_data['hours'][days[current]]['open'] = 'closed'
							new_data['hours'][days[current]]['close'] = 'closed'
					section_line = 0
					new_data['tags'] = 'food'
					result_post.append(new_data)
	return result_post

'''
building_data_template = {
	'name': '',
	'building_code': '',
	'cover_polygon': [
		{
			'lon': 0,
			'lat': 0
		}
	],
	'location': {
		'lon': 0,
		'lat': 0
	},
	'year_built': 0,
	'history': '',
}
'''
def get_building_db():
	result_post=[]
	with open('txt_files/building_list.txt', 'rU') as f:
		for line in f:
			if line.strip():
				
				new_data = copy.deepcopy(building_data_template)
				sections = line.split(',')
				
				new_data['name'] = sections[0].strip()
				new_data['building_code'] = sections[1].strip()
				try:
					new_data['location']['lon'] = sections[2].strip()
					new_data['location']['lat'] = sections[3].strip()
				except:
					pass
				try:
					
					for i in sections[4].split('|'):
						temp_coord = {'lon': 0, 'lat': 0}
						temp_coord['lon'] = i.split('&')[0].strip()
						temp_coord['lat'] = i.split('&')[1].strip()
						new_data['cover_polygon'].append(temp_coord)
				except:
					pass
				result_post.append(new_data)
	return result_post

def populate_subject_db():
	for i in get_subject_db():	
		r = requests.post('http://127.0.0.1:1337/subjects/', data=json.dumps(i), headers=headers)
		if r.status_code != 200:
			r = requests.put('http://127.0.0.1:1337/subjects/', data=json.dumps(i), headers=headers)

def populate_course_db():
	for i in get_course_db():	
		print i
		break
	'''
	for i in get_course_db():	
		r = requests.post('http://127.0.0.1:1337/courses/', data=json.dumps(i), headers=headers)
		if r.status_code != 200:
			r = requests.put('http://127.0.0.1:1337/courses/', data=json.dumps(i), headers=headers)
	'''
def populate_restaurant_db():
	for i in get_restaurant_db():	
		print i['name'] + ' in building: ' + i['building']
		r = requests.post('http://127.0.0.1:1337/places/restaurants', data=json.dumps(i), headers=headers)
		if r.status_code != 200:
			r = requests.put('http://127.0.0.1:1337/places/restaurants', data=json.dumps(i), headers=headers)

def populate_building_db():
	for i in get_building_db():	
		#print i['name'] + 'in building: ' + i['building']
		r = requests.post('http://127.0.0.1:1337/places/buildings', data=json.dumps(i), headers=headers)
		if r.status_code != 200:
			r = requests.put('http://127.0.0.1:1337/places/buildings', data=json.dumps(i), headers=headers)

def test():
	pass
	#r = requests.post('http://127.0.0.1:1337/courses/', data={'credit_count': 3, 'description': '', 'title': 'Introduction To Financial Accounting I', 'course_subject': 'ACTG', 'year_level': 2, 'term_year': 1415, 'course_number': '2010', 'faculty': 'SB', 'course_code': 'ACTG2010', 'terms_offered': [{'terms': ['W or F'], 'term_year': 1415}]})
	#r = requests.post('http://127.0.0.1:1337/courses/', data={'credit_count': 4, 'description': '', 'title': 'Introduction To Financial Accounting I', 'course_subject': 'ACTG', 'year_level': 2, 'course_number': '2010', 'faculty': 'SB', 'course_code': 'ACTG2010', 'terms_offered': 1415}})
	#r = requests.put('http://127.0.0.1:1337/courses/', data={'credit_count': 99, 'description': '', 'title': 'Introduction To Financial Accounting I', 'course_subject': 'ACTG', 'year_level': 2, 'instructors': '', 'term_year': 1415, 'course_number': '2010', 'faculty': 'SB', 'course_code': 'ACTG2010', 'terms_offered': [{'terms': ['W or F'], 'term_year': 1415}]})
	
def main(argv):
	try:
		opts, args = getopt.getopt(argv,"htp:",["populate="])
	except getopt.GetoptError:
		print 'post_client.py -p <db_document>'
		sys.exit(2)
	if not opts:
		print "post_client.py -p <db_document>"
	else:
		for opt, arg in opts:	
			if opt == '-h':
				print 'post_client.py -p <db_document>'
				sys.exit()
			elif opt in ("-p", "--populate"):
				if (arg == 'courses'):
					print "Populating Course db..."
					populate_course_db()
				if (arg == 'subjects'):
					print "Populating Subjects db..."
					populate_subject_db()
				if (arg == 'buildings'):
					print "Populating Building db..."
					populate_building_db()
				if (arg == 'restaurants'):
					print "Populating Restaurant db..."
					populate_restaurant_db()
					
if __name__ == "__main__":
   main(sys.argv[1:])

	
	
	
	