import sys, getopt
import requests
import hashlib
import json
from datetime import datetime

def remember_new(data_type, new_data):
    valid = {"yes": True, "y": True, "Y": True, 
    		"no": False, "n": False, "N": False}

    while True:
        print(f"Remember new {data_type}? [Y/n]")
        choice = input().lower()
        if choice == '':
            answer = True
            break
        elif choice in valid:
            answer = valid[choice]
            break
        else:
        	print("Please respond with 'Y' or 'N' (or 'y' or 'n').\n")
    if answer:
    	with open('config.ini', encoding="utf-8") as f:
    		tempdata = json.load(f)
    	tempdata[data_type] = new_data
    	with open('config.ini', 'w', encoding="utf-8") as f:
    		json.dump(tempdata, f)

def date_recog(d):
	if d == 'today':
		return datetime.today().strftime("%Y-%m-%d")
	else:
		for fmt in ['%d-%m-%Y', '%d.%m.%y', 
					'%d.%m.%Y', '%Y-%m-%d', 
					'%d/%m/%y', '%d/%m/%Y']:
			try:
				return datetime.strptime(d, fmt).strftime("%Y-%m-%d")
			except ValueError:
				pass
		sys.exit("Try another date format with year or 'today'")



def main(argv):	
	#Загрузка сохранённых аргументов
	with open('config.ini', encoding="utf-8") as f:
		data = json.load(f)

	#Обработка и получение логина, пароля, даты и группы из агрументов cmd
	try:
		opts, args = getopt.getopt(argv, "hd:l:p:g:", ["date=", "login=", "password=", "group="])
	except getopt.GetoptError:
		sys.exit("Nashagai.py -d <YYYY-MM-DD> -l <login/email> -p <password> -g <group>")

	date = date_recog('today')

	for opt, arg in opts:
		if opt == '-h':
			print ("Nashagai.py -d <YYYY-MM-DD> -l <login/email> -p <password> -g <group>")
			sys.exit()

		elif opt in ("-d", "--date"):
			date = date_recog(arg)

		elif opt in ("-l", "--login"):
			if data['login'] != arg:
				data['login'] = arg
				remember_new('login', arg)

		elif opt in ("-p", "--password"):
			if data['password'] != arg:
				data['password'] = arg
				remember_new('password', arg)

		elif opt in ("-g", "--group"):
			if data['group'] != arg:
				data['group'] = arg
				remember_new('group', arg)
	#Если какие-то данные отсутсвуют
	for dtype in ['login', 'password', 'group']:
		if data[dtype] == '':
			print(f'{dtype} is empty! Please, type it:')
			data[dtype] = input()
			remember_new(dtype, data[dtype])

	#Создание payload и headers
	hash_object = hashlib.md5(data['password'].encode())
	encrypted_pass = hash_object.hexdigest()
	payload = {
	    'email': data['login'],
	    'password': encrypted_pass
	}
	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
	}


	with requests.Session() as s:
		loginUrl = 'https://www.mypacer.com/api/v1/auth'
		requestUrl = f'https://www.mypacer.com/api/v1/organizations/74509/activity/ranks?start_date={date}&end_date={date}&data_type=steps&statistic_type=total&activity_detail=true'
		
		try:
			r = s.post(loginUrl, data = payload, headers = headers)
		except requests.exceptions.ConnectionError:
			sys.exit("Log in failed")
		if '"success": true' in r.text[:50]:
			print("Logged in!")
		else:
			sys.exit("Log in failed")

		r = s.get(requestUrl, headers = headers)
		accounts = r.json()['data']['rank_accounts']

	for account in accounts:
		if account['group_name'] == data['group']:
			print(account['info']['display_name'],' --- ', account['data_value'])

if __name__ == "__main__": 
	main(sys.argv[1:])
