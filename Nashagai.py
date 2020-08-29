import sys, getopt
import requests
import hashlib
import json
from datetime import datetime

def main(argv):	
	#Стандартные аргументы
	login = 'qt74509'
	password = 'zwvemvrx'
	date = datetime.today().strftime("%Y-%m-%d")
	group = 'Куратор Антон Паймин'

	#Обработка аргументов
	try:
		opts, args = getopt.getopt(argv, "hd:l:p:g:", ["date=", "login=", "password=", "group="])
	except getopt.GetoptError:
		print ('Nashagai.py -d <YYYY-MM-DD> -l <login/email> -p <password> -g <group>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('Nashagai.py -d <YYYY-MM-DD> -l <login/email> -p <password> -g <group>')
			sys.exit()
		elif opt in ("-d", "--date"):
			try:
				datetime.strptime(arg, '%Y-%m-%d')
			except ValueError:
				print("Incorrect data format, should be YYYY-MM-DD")
				sys.exit()
			date = arg
		elif opt in ("-l", "--login"):
			login = arg
		elif opt in ("-p", "--password"):
			password = arg
		elif opt in ("-g", "--group"):
			group = arg

	#Создание payload и headers
	hash_object = hashlib.md5(password.encode())
	encrypted_pass = hash_object.hexdigest()
	payload = {
	    'email': login,
	    'password': encrypted_pass
	}

	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
	}


	with requests.Session() as s:
		loginUrl = 'https://www.mypacer.com/api/v1/auth'
		requestUrl = f'https://www.mypacer.com/api/v1/organizations/74509/activity/ranks?start_date={date}&end_date={date}&data_type=steps&statistic_type=total&activity_detail=true'
		
		r = s.post(loginUrl, data = payload, headers = headers)
		if '"success": true' in r.text[:50]:
			print('Logged in!\n')
		else:
			print('Log in failed \nClosing...')
			sys.exit()

		r = s.get(requestUrl, headers = headers)
		accounts = r.json()['data']['rank_accounts']


	for account in accounts:
		if account['group_name'] == group:
			print(account['info']['display_name'],' --- ', account['data_value'])



if __name__ == "__main__": 
	main(sys.argv[1:])
