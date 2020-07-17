# app.py
from flask import Flask, request, jsonify

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time
import random 
import io
import os
import threading
from firebase import firebase

from flask_cors import CORS
import flask

import common
import database

app = Flask(__name__) 
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) 
# @cross_origin()

@app.route('/api/booking/', methods=['GET','POST'])
def booking():
    if flask.request.method == 'POST': 
        id = request.form.get('id')
        store = request.form.get('store')
        pid = request.form.get('pid')
        size = request.form.get('size')
        amount = request.form.get('amount')
    else: 
        id = request.args.get('id')
        store = request.args.get('store')
        pid = request.args.get('pid')
        size = request.args.get('size')
        amount = request.args.get('amount') 

    print(id,store,pid,size,amount)

    response = {}  
    response["MESSAGE"] = f"Booking finish 1 time!!"
    
    # store = 'architectureandsneakers'
    # pid = '151555065'
    # size = '27.0'
    # amount = 1
    print('start booking', id)

    xxx = threading.Thread(target=common.booking, args=(store, pid, size, amount, id))
    xxx.start()
    xxx.join() 
    print('end booking', id)

    # Return the response in json format
    return jsonify([response])


@app.route('/api/test/', methods=['GET','POST'])
def test():  
    id = '3ckOjcgHN2Mrpm3VzI3z'
    
    result = database.update_status(id) 

    response = {}  
    response["MESSAGE"] = result 
 

    # Return the response in json format
    return jsonify([response])


@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

# @app.route('/post/', methods=['POST'])
# def post_something():
#     param = request.form.get('name')
#     print(param)
#     # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
#     if param:
#         return jsonify({
#             "Message": f"Welcome {name} to our awesome platform!!",
#             # Add this option to distinct the POST request
#             "METHOD" : "POST"
#         })
#     else:
#         return jsonify({
#             "ERROR": "no name found, please send a name."
#         })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)