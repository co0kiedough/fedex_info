from fedex_creds import *
import json
import requests
import glob
import csv


class fedex_track:
	
	def __init__(self):
		self.url = "https://apis-sandbox.fedex.com/oauth/token"
		
		self.credentials = creds()
		self.cdict = self.credentials.get_creds()
		self.payload={"grant_type": "client_credentials",'client_id':self.cdict['client_id'],'client_secret':self.cdict['client_secret']}

	
		self.headers = {'Content-Type': "application/x-www-form-urlencoded"}
		self.response= requests.post(self.url, data=(self.payload), headers=self.headers)
	
	def auth_token(self):
		
		token = json.loads(self.response.text)['access_token']
		
		return token
	
	def get_ship_info(self, token):
		
		ing = glob.glob('*tack*.csv')
		inf = open(ing[0], 'r', newline='')
		payload = {"includeDetailedScans": 'true'}
		payload['trackingInfo'] = []
		inc = csv.DictReader(inf)
		payload['trackingInfo'].append({'trackingNumberInfo':{'trackingNumber':row['Tracking Number']} for row in inc})
		url = 'https://developer.fedex.com/api/en-us/catalog/track/v1/track/v1/trackingnumbers'
		token = self.auth_token()
		
		headers = { \
			'Content-Type': "application/json", \
			'X-locale': "en_US", \
			'Authorization': 'Bearer '+ token \
		}

		
		response = requests.post(url, data=payload, headers=headers)
		
		return response

	

