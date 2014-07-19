#!ve/bin/python
import requests
import json
import copy

abrv_to_full_course_subjects = {
'''
	ADMB - Administrative Studies Bridging - ( AP ) 
	ADMS - Administrative Studies - ( AP ) 
	ANTH - Anthropology - ( AP, GS ) 
	ARB - Arabic - ( AP ) 
	ARTH - Art History - ( FA, GS ) 
	ASL  - Asl  American Sign Language - ( AP ) 
	BC   - Bethune College - ( SC ) 
	BCHM - Biochemistry - ( SC ) 
	BIOL - Biology - ( SC ) 
	BLIS - International Business Law - ( GS ) 
	BSUS - Business and Sustainability - ( SB ) 
	BUEC - Business Economics - ( GL ) 
	CDIS - Critical Disability - ( GS ) 
	CDNS - Canadian Studies - ( AP, GL ) 
	CH   - Chinese - ( AP ) 
	CHEM - Chemistry - ( GS, SC ) 
	CLTR - Culture - ( AP ) 
	CMCT - Communication and Culture - ( GS ) 
	CMYR - Common Year - ( ED ) 
	COMN - Communication Studies - ( AP ) 
	COOP - Cooperative Education - ( SC ) 
	CRIM - Criminology - ( AP ) 
	CSE - Computer Science & Engineering - ( GS, LE ) 
	DANC - Dance - ( FA, GS ) 
	DEMS - Disaster and Emergency Management - ( GS ) 
	DRST - Drama Studies - ( GL ) 
	DVST - Development Studies Graduate Program - ( GS ) 
	EATS - Earth & Atmos. Science - ( LE ) 
	ECON - Economics - ( AP, GL, GS, SB ) 
	EDUC - Education - ( ED, GS ) 
	EMBA - Executive Masters Business Administration - ( SB ) 
	EN   - English - ( AP, GL, GS ) 
	ENG - Engineering - ( LE ) 
	ENTR - Entrepreneurial Studies - ( SB ) 
	ENVB - Environmental Biology - ( SC ) 
	ENVS - Environmental Studies - ( ES ) 
	ESL  - English As A Second Language - ( AP ) 
	ESS  - Earth & Space Science - ( GS ) 
	ETHC - Business Ethics - ( SB ) 
	EXCH - Exchange - ( SB ) 
	FACC - Financial Accountability - ( GS ) 
	FACS - Fine Arts Cultural Studies - ( FA ) 
	FILM - Film - ( FA, GS ) 
	FINE - Finance - ( SB ) 
	FNEN - Financial Engineering - ( SB ) 
	FNSV - Financial Services - ( SB ) 
	FR   - French Studies - ( AP ) 
	FRAN - French Studies/Etudes Francaises  - ( GL ) 
	FREN - French - ( GS ) 
	FRLS - Francais Langue Seconde - ( GL ) 
	FSL - French As A Second Language - ( GL ) 
	GEOG - Geography - ( AP, GS, SC ) 
	GER  - German - ( AP ) 
	GFWS - Gender, Feminist and Womens Studies - ( GS ) 
	GWST - Gender and Women's Studies - ( AP, GL ) 
	HIMP - Health Industry Management Program - ( SB ) 
	HIST - History - ( AP, GL ) 
	HLST - Health Studies - ( HH ) 
	HLTH - Health - ( GS ) 
	HREQ - Human Rights and Equity Studies - ( AP ) 
	HRM - Human Resources Management - ( AP, GS ) 
	HUMA - Humanities - ( AP, GL, GS ) 
	IBUS - International Business - ( SB ) 
	IHST - Global Health - ( HH ) 
	ILST - International Studies - ( GL ) 
	INLE - Inquiries into Learning - ( ED ) 
	INST - Interdisciplinary Study - ( GS ) 
	INTE - Conference Interpreting - ( GS ) 
	INTL - International - ( SB ) 
	IT   - Italian - ( AP ) 
	ITEC - Information Technology - ( AP, GS ) 
	JC - Jamaican Creole - ( AP ) 
	KAHS - Kinesiology & Health Science - ( GS ) 
	KINE - Kinesiology & Health Science - ( HH ) 
	LAL - Linguistics and Applied Linguistics - ( GS ) 
	LAW  - Law - ( GS ) 
	LIN - Linguistics and Language Studies - ( GL ) 
	LING - Linguistics - ( AP ) 
	LREL - Labour Relations and Employment Law - ( GS ) 
	MACC - Master of Accounting - ( SB ) 
	MATH - Mathematics and Statistics - ( GS, SC ) 
	MFIN - Master of Finance - ( SB ) 
	MGMT - Management - ( SB ) 
	MIST - Multicultural and Indigenous Studies - ( AP ) 
	MKTG - Marketing - ( SB ) 
	MODR - Modes Of Reasoning - ( AP, GL ) 
	MSBA - Master of Science in Business Analytics - ( SB ) 
	MUSI - Music - ( FA, GS ) 
	NATS - Natural Science - ( GL, SC ) 
	NURS - Nursing - ( GS, HH ) 
	OMIS - Operations Management and Information Syste - ( SB ) 
	ORGS - Organization Studies - ( SB ) 
	OVGS - Ont.Visiting Graduate Student - ( GS ) 
	PHIL - Philosophy - ( AP, GL, GS ) 
	PHYS - Physics and Astronomy - ( GS, SC ) 
	PIA - Public and International Affairs - ( GS ) 
	PKIN - Kinesiology & Health Sc Pract - ( HH ) 
	POLS - Political Science - ( AP, GL, GS ) 
	POR  - Portuguese - ( AP ) 
	PPAL - Public Policy Administration & Law - ( GS ) 
	PPAS - Public Policy and Administration Studies - ( AP ) 
	PRAC - Practicum - ( ED ) 
	PROP - Real Property - ( SB ) 
	PSYC - Psychology - ( GL, GS, HH ) 
	PUBL - Public Administration - ( SB ) 
	RYER - Ryerson - ( AP ) 
	SGMT - Strategic Management - ( SB ) 
	SLST - Socio-Legal Studies - ( GS ) 
	SOCI - Sociology - ( AP, GL, GS ) 
	SOSC - Social Science - ( AP, GL ) 
	SOWK - Social Work - ( AP, GS ) 
	SP   - Spanish - ( AP ) 
	SPTH - Social & Political Thought - ( GS ) 
	STS  - Science and Technology Studies - ( SC ) 
	THEA - Theatre - ( FA, GS ) 
	THST - Theatre Studies - ( GS ) 
	TRAN - Translation - ( GL, GS ) 
	URST - Urban Studies - ( AP ) 
	VISA - Visual Arts - ( FA, GS ) 
	WMST - Womens Studies - ( GS ) 
	WRIT - Writing - ( AP ) 
	YSDN - York/Sheridan Design - ( FA ) 
'''
}

if __name__ == '__main__':
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

	term_offered_template = {'term_year': 0, 'terms': []}

	#
	#fo = open("course_list.txt", "rw+")
	#line = fo.readline()

	term_year = 1415
	term = "W or F"



	#print json.dumps(new_data, sort_keys=True, indent=4, separators=(',', ': '))
	with open('course_list.txt', 'rU') as f:
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

				r = requests.post('http://127.0.0.1:5000/courses/', data=json.dumps(new_data))
		