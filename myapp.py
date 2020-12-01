# myapp.py
''' 
    This file is based off of this tutorial: https://stackabuse.com/deploying-a-flask-application-to-heroku/ 
    Author: Chandra Krintz, 
    License: UCSB BSD -- see LICENSE file in this repository
'''

import os, json
from flask import Flask, request, jsonify, make_response, abort, redirect, url_for
from database import db, User, Course
import psycopg2

DEBUG=True

#use this if linking to a reaact app on the same server
#app = Flask(__name__, static_folder='./build', static_url_path='/')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(__file__),'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

if False:
    with app.app_context():
        # Resetting database for now since format changes are expected
        db.drop_all()
        # Mockup of database
        db.create_all()
        print('Reset database')

#deprecated
from api import api_v1
app.register_blueprint(api_v1,url_prefix='/api/v1/')
#---

from api2 import initialize_routes
from flask_restful import Api
api = Api(app)
initialize_routes(api)

### CORS section
@app.after_request
def after_request_func(response):
    if DEBUG:
        print("in after_request")
    #origin = request.headers.get('Origin')
    origin = '*'
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
        response.headers.add('Access-Control-Allow-Methods',
                            'GET, POST, OPTIONS, PUT, PATCH, DELETE')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)
    else:
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)

    return response
### end CORS section

'''
Note that flask automatically redirects routes without a final slash (/) to one with a final slash (e.g. /getmsg redirects to /getmsg/). Curl does not handle redirects but instead prints the updated url. The browser handles redirects (i.e. takes them). You should always code your routes with both a start/end slash.
'''

# Set the base route to be the react index.html
@app.route('/')
def index():
    return redirect(url_for('users'))

def main():
    '''The threaded option for concurrent accesses, 0.0.0.0 host says listen to all network interfaces (leaving this off changes this to local (same host) only access, port is the port listened on -- this must be open in your firewall or mapped out if within a Docker container. In Heroku, the heroku runtime sets this value via the PORT environment variable (you are not allowed to hard code it) so set it from this variable and give a default value (8118) for when we execute locally.  Python will tell us if the port is in use.  Start by using a value > 8000 as these are likely to be available.
    '''
    localport = int(os.getenv("PORT", 8118))
    app.run(threaded=True, host='0.0.0.0', port=localport)

if __name__ == '__main__':
    main()
