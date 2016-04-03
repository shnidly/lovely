# https://github.com/mimming/python-flask-google-api-starter/blob/master/cal.py
# https://developers.google.com/api-client-library/python/auth/web-app#example

import os  # Required for Heroku

import apiclient
import httplib2
from oauth2client import client

import datetime

from flask import Flask, render_template, session, request, redirect, url_for
from flask.ext.pymongo import PyMongo

import db_manager

app = Flask(__name__)
mongo = PyMongo(app)

CLIENT_ID = "788402987571-lkij3nh54tlp35g82h3b94ktj6gl529g.apps.googleusercontent.com"
CLIENT_SECRET = '0EXqx_OQbJYRw-TavXBftK60'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register_form', methods=['POST'])
def register_form():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    print(mongo.db.users.insert_one(db_manager.gen_new_user(username, password, email)))

    session['username'] = username
    return redirect(url_for('dashboard'))


@app.route('/login')
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/login_form', methods=['POST'])
def login_form():
    username = request.form['username']
    password = request.form['password']

    cursor = mongo.db.users.find({"username": username})

    for user in cursor:
        print(user)

        if user['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))

    return redirect(url_for('index'))


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        cursor = mongo.db.contacts.find({'owner': session['username']})

        contact_dict = {}  # List
        for contact in cursor:
            print(contact)
            contact_dict[str(contact['_id'])] = contact['name']

        return render_template('dashboard.html', username=session['username'], contact_dict=contact_dict)

    return redirect(url_for('index'))


@app.route('/wipedb')
def wipedb():
    mongo.db.users.remove({})
    mongo.db.contacts.remove({})
    return redirect(url_for('logout'))


@app.route('/generate')
def generate():
    if 'username' not in session:
        print("Please sign in.")
        return redirect(url_for('index'))

    owner = session['username']

    print(mongo.db.contacts.insert_many([
        db_manager.gen_new_contact(owner, 'John Appleseed', 234567890, -5),
        db_manager.gen_new_contact(owner, 'Anne Smith', 8003234555, -8),
        db_manager.gen_new_contact(owner, 'Steven Berg', 9463112232, +4.75),
        db_manager.gen_new_contact(owner, 'Elora Szeto', 7163831103, 0),
        db_manager.gen_new_contact(owner, 'Eric Sayer', 1234569999, 2)]))
    return redirect(url_for('dashboard'))


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
    session.pop('username', None)
    session.pop('credentials', None)
    session['message'] = "You have logged out."

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.secret_key = "Love.ly"
    app.run(host='0.0.0.0', port=port, debug=True)
