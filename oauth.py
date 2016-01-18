import ConfigParser
import requests
import json


class data:	pass
dat = data()

"""
https://developer.paypal.com/docs/integration/direct/paypal-oauth2/?mark=oauth
https://developer.paypal.com/docs/integration/direct/make-your-first-call/

curl -v https://api.sandbox.paypal.com/v1/oauth2/token \
-H "Accept: application/json" \
-H "Accept-Language: en_US" \
-u "client_id:secret_id" \
-d "grant_type=client_credentials"

"""

class paypal_api:
	'Holds methods using REST API paypal by access token'

	def __init__(self,token):
		self.access_token = token

	def user_creditials(self):

		header = {'Content-Type': 'application/json','Authorization': 'Bearer '+ self.access_token}
		url = dat.base_url + '/v1/identity/openidconnect/userinfo/?schema=openid'
		response = requests.post(url=url,headers=header)

		if response.status_code != 200:
			return 'error'

		return response.text


def get_access_token():

	headers = {'Accept': 'application/json','Accept-Language': 'en_US'}
	url = dat.base_url + '/v1/oauth2/token'
	auth = (dat.client_id,dat.secret_id)
	data = {'grant_type': 'client_credentials','redirect_uri': dat.redirect_uri}
	response = requests.post(url,data=data,headers=headers,auth=auth)

	if response.status_code != 200:
		return 'error'

	access_token = response.json()["access_token"]
	return access_token

def conf():	
	config = ConfigParser.ConfigParser()
	configfile = 'data.conf'
	config.read(configfile)
	dat.client_id = config.get('paypal','client_id')
	dat.secret_id = config.get('paypal','secret_id')
	dat.account = config.get('sandbox','account')
	dat.pswd = config.get('sandbox','pswd')
	dat.base_url = config.get('URL','api_url')
	dat.redirect_uri = config.get('URL','redirect')

def main():
	conf()
	access_token = get_access_token()
	if access_token != 'error':
		api = paypal_api(access_token)
		user_info = api.user_creditials()
		print 'access token: ',access_token
		print 'user info: ', user_info

if __name__ == '__main__':
    main()