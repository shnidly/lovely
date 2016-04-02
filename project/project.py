# https://github.com/mimming/python-flask-google-api-starter/blob/master/cal.py

# Required for Heroku
import os
# Google API imports
import apiclient
import httplib2
# OAuth imports
from oauth2client.client import OAuth2WebServerFlow
# Flask imports
from flask import Flask, render_template, session, request, redirect, url_for

app = Flask(__name__)

CLIENT_ID = "788402987571-lkij3nh54tlp35g82h3b94ktj6gl529g.apps.googleusercontent.com"
CLIENT_SECRET = '0EXqx_OQbJYRw-TavXBftK60'


@app.route('/login')
def login():
    flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                               client_secret=CLIENT_SECRET,
                               scope='https://www.googleapis.com/auth/calendar',
                               redirect_uri='https://lovely-hackprinceton.herokuapp.com:'
                                            + os.environ.get('PORT', 5000) + '/oauth2callback',
                               approval_prompt='force',
                               access_type='offline')

    auth_uri = flow.step1_get_authorize_url()
    return redirect(auth_uri)


@app.route('/signout')
def signout():
    del session['credentials']
    session['message'] = "You have logged out"

    return redirect(url_for('index'))


@app.route('/oauth2callback')
def oauth2callback():
    code = request.args.get('code')

    if code:
        # exchange the authorization code for user credentials
        flow = OAuth2WebServerFlow(CLIENT_ID,
                                   CLIENT_SECRET,
                                   "https://www.googleapis.com/auth/calendar")
        flow.redirect_uri = request.base_url

        try:
            credentials = flow.step2_exchange(code)
        except Exception as e:
            print("Unable to get an access token because ", e.message)

        # store these credentials for the current user in the session
        # This stores them in a cookie, which is insecure. Update this
        # with something better if you deploy to production land
        session['credentials'] = credentials

    return redirect(url_for('index'))


@app.route('/')
def index():
    credentials = session['credentials']

    if credentials is None:
        return redirect(url_for('login'))

    http = httplib2.Http()
    http = credentials.authorize(http)
    service = apiclient.discovery.build("calendar", "v3", http=http)
    calendar_list = service.calendarList().list().execute()

    return render_template("index.html", calendar_list=calendar_list)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.secret_key = "Love.ly"
    app.run(host='0.0.0.0', port=port, debug=True)


