from flask import Flask, redirect, request
import requests
import ConfigParser
import requests.auth
import json
from data import secret_key, client_id

redirect_uri = r"http://127.0.0.1:5000/app"
auth_url = r"https://www.sandbox.paypal.com/webapps/auth/protocol/openidconnect/v1/authorize"
api_url = r'https://api.sandbox.paypal.com/v1/identity/openidconnect'

application = Flask(__name__)

@application.route("/")
def index():

    resp_type = "code"
    scope = "openid"
    reqtext = auth_url + "?client_id=" + client_id +\
    "&response_type=" + resp_type +\
    "&scope=" + scope +\
    "&redirect_uri=" + redirect_uri

    return redirect(reqtext, 302)

@application.route("/app", methods=['GET'])
def app():
    """
    Getting authorization_code
    """
    confirm_code = request.args.get('code')
    if confirm_code is None:
        return "bad request"

    auth = (client_id, secret_key)
    url = api_url + r'/tokenservice'
    params = {'grant_type': 'authorization_code', 'code': confirm_code, 'redirect_uri': redirect_uri}
    """
    Getting an access_token
    """
    response = requests.post(url=url, auth=auth, data=params)
    if response.status_code // 100 != 2:
        return "Wrong auth"

    access_token = response.json()["access_token"]
    #print(access_token)

    """
    Using paypal REST API
    """
    url = api_url + r'/userinfo/?schema=openid'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token}

    response = requests.get(url=url, headers=headers)
    if response.status_code // 100 != 2:
        print(response.status_code)
        return "Internal request error"

    text = response.text
    return text

if __name__ == "__main__":
    application.run()
