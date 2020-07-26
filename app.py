# app.py
from flask import Flask, request, jsonify

import threading

from flask_cors import CORS
import flask

import common
# import database

app = Flask(__name__) 
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.route('/api/booking/', methods=['GET','POST'])
def booking():
    if flask.request.method == 'POST':
        id = request.form.get('id')
        card_number = request.args.get('card_number')
        cardholder = request.args.get('cardholder')
        exp_m = request.args.get('exp_m')
        exp_y = request.args.get('exp_y')
        cvv = request.args.get('cvv')
    else:
        id = request.args.get('id')
        card_number = request.args.get('card_number')
        cardholder = request.args.get('cardholder')
        exp_m = request.args.get('exp_m')
        exp_y = request.args.get('exp_y')
        cvv = request.args.get('cvv')

    print(id, card_number, cardholder, exp_m, exp_y, cvv)

    response = {}  
    response["MESSAGE"] = f"Booking finish 1 time!!"

    common.booking_tokyo(card_number, cardholder, exp_m, exp_y, cvv, id)
    # xxx = threading.Thread(target=common.booking_tokyo, args=(card_number, cardholder, exp_m, exp_y, cvv, id))
    # xxx.start()
    # xxx.join()

    # Return the response in json format
    return jsonify([response])


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)