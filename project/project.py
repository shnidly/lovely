# https://github.com/mimming/python-flask-google-api-starter/blob/master/cal.py
# https://developers.google.com/api-client-library/python/auth/web-app#example

import os  # Required for Heroku

import apiclient
import httplib2
from oauth2client import client

import datetime

from flask import Flask, render_template, session, request, redirect, url_for
import db_comm

app = Flask(__name__)

CLIENT_ID = "788402987571-lkij3nh54tlp35g82h3b94ktj6gl529g.apps.googleusercontent.com"
CLIENT_SECRET = '0EXqx_OQbJYRw-TavXBftK60'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/cal')
def cal():
    # Check if credentials exist within session.
    if 'credentials' not in session:
        return redirect(url_for('oauth2callback'))

    # Convert json credentials stored to a OAuth2Credentials object
    credentials = client.OAuth2Credentials.from_json(session['credentials'])

    # If the credentials are expired, they're might as well nonexistent!
    if credentials.access_token_expired:
        return redirect(url_for('oauth2callback'))
    else:
        http_auth = httplib2.Http()
        http_auth = credentials.authorize(http_auth)
        service = apiclient.discovery.build('calendar', 'v3', http_auth)

        '''
        Shows basic usage of the Google Calendar API.

            Creates a Google Calendar API service object and outputs a list of the next
            10 events on the user's calendar.
        '''

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

        events_result = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        return render_template('calendar.html', events=events)


@app.route('/oauth2callback')
def oauth2callback():
    # Exchange the authorization code for user credentials
    flow = client.OAuth2WebServerFlow(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope='https://www.googleapis.com/auth/calendar',
        redirect_uri=url_for('oauth2callback', _external=True),
        access_type='offline'
    )

    # If a credential code is not received from Google yet, send them to get it.
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)

    # Otherwise, authenticate the user.
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)

        # Convert credentials to json because that is the only way to store it in a session.
        session['credentials'] = credentials.to_json()

        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    del session['credentials']
    session['message'] = "You have logged out."

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.secret_key = "Love.ly"
    app.run(host='0.0.0.0', port=port, debug=True)
