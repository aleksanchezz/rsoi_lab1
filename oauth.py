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


auth = requests.auth.HTTPBasicAuth(client_id, secret_key)
    url = r'https://api.sandbox.paypal.com/v1/identity/openidconnect/tokenservice'
    params = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri}

    response = requests.post(url=url, auth=auth, data=params)

params = {
    'arg1': 'demo',
    'arg2': 'password',
    'arg3': 'demo@gmail.com',
}
auth = ('admin', 'p4ssw0rd')
url = 'https://server.vestacp.com:8083/api/'
r = requests.post(url, params=params, auth=auth)
if r.text == 0:
    print('OK')
else:
    print('Error code: %s' % r.text)

client_credentials
authorization_code
"""

class paypal_api:
	'Hols methods using REST API paypal by access token'

	def __init__(self,token):
		self.access_token = token

	def user_creditials(self,login,pswd):
		print login,'  ',pswd

def get_access_token():

	headers = {'Accept': 'application/json','Accept-Language': 'en_US'}
	auth = (dat.client_id,dat.secret_id)
	data = {'grant_type': 'client_credentials','redirect_uri': dat.redirect_uri}
	response = requests.post(dat.url,data=data,headers=headers,auth=auth)

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
	dat.url = config.get('URL','direct')
	dat.redirect_uri = config.get('URL','redirect')

def main():
	conf()
	access_token = get_access_token()
	if access_token != 'error':
		api = paypal_api(access_token)
		api.user_creditials(dat.account,dat.pswd)


if __name__ == '__main__':
    main()