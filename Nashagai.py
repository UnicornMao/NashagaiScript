import requests
import hashlib
import json
from datetime import datetime

password = 'zwvemvrx'
hash_object = hashlib.md5(password.encode())
encrypted_pass = hash_object.hexdigest()
payload = {
    'email': 'qt74509',
    'password': encrypted_pass
}

headers = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}

with requests.Session() as s:
	loginUrl = 'https://www.mypacer.com/api/v1/auth'
	today = datetime.today().strftime("%Y-%m-%d")
	print(today)
	requestUrl = f'https://www.mypacer.com/api/v1/organizations/74509/activity/ranks?start_date={today}&end_date={today}&data_type=steps&statistic_type=total&activity_detail=true'
	
	r = s.post(loginUrl, data = payload, headers = headers)
	print('Logged in!\n')

	r = s.get(requestUrl, headers = headers)
	print('Got the response! \n')

	accounts = r.json()['data']['rank_accounts']

for account in accounts:
	if account['group_name'] == 'Куратор Антон Паймин':
		print(account['info']['display_name'],' --- ', account['data_value'])
