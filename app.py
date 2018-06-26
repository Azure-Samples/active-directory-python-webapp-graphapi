from adal import AuthenticationContext
from flask import (Flask, redirect, url_for,
                   Response, session)

import flask
import uuid
import requests
import config

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

PORT = 5000  # A flask app by default runs on PORT 5000
AUTHORITY_URL = config.AUTHORITY_HOST_URL + '/' + config.TENANT
REDIRECT_URI = 'http://localhost:{}/getAToken'.format(PORT)
TEMPLATE_AUTHZ_URL = ('https://login.microsoftonline.com/{}/oauth2/authorize?' +
                      'response_type=code&client_id={}&redirect_uri={}&' +
                      'state={}&resource={}')


@app.route("/")
def main():
    login_url = 'http://localhost:{}/login'.format(PORT)
    resp = Response(status=307)
    resp.headers['location'] = login_url
    return resp


@app.route("/login")
def login():
    auth_state = str(uuid.uuid4())
    session['state'] = auth_state
    authorization_url = TEMPLATE_AUTHZ_URL.format(
        config.TENANT,
        config.CLIENT_ID,
        REDIRECT_URI,
        auth_state,
        config.RESOURCE)
    resp = Response(status=307)
    resp.headers['location'] = authorization_url
    return resp


@app.route("/getAToken")
def main_logic():
    code = flask.request.args['code']
    state = flask.request.args['state']
    if state != session['state']:
        raise ValueError("State does not match")
    auth_context = AuthenticationContext(AUTHORITY_URL)
    token_response = auth_context.acquire_token_with_authorization_code(code, REDIRECT_URI, config.RESOURCE,
                                                                        config.CLIENT_ID, config.CLIENT_SECRET)
    session['access_token'] = token_response['accessToken']

    return flask.redirect('/graphcall')


@app.route('/graphcall')
def graphcall():
    if 'access_token' not in session:
        return redirect(url_for('login'))
    endpoint = config.RESOURCE + '/' + config.API_VERSION + '/me/'
    http_headers = {'Authorization': session.get('access_token'),
                    'User-Agent': 'adal-python-sample',
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'client-request-id': str(uuid.uuid4())}
    graph_data = requests.get(endpoint, headers=http_headers, stream=False).json()
    return flask.render_template('display_graph_info.html', graph_data=graph_data)


if __name__ == "__main__":
    app.run()
