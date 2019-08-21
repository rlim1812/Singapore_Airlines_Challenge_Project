# import necessary packages
from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS
import simplejson as json
import sqlite3
import pandas as pd
from dateutil import parser
from pmdarima.arima import auto_arima

# create Flask app
app = Flask(__name__)
cors = CORS(app)

# form connection to database
conn = sqlite3.connect('EnergyConsumption.db')
cur = conn.cursor()

@app.route("/")
def index():
    return render_template("index.html")

# set up route for front end to get LBNL electricity data from the database
@app.route('/electricity_data')
def get_electricity_data():
    # form connection to database
    conn = sqlite3.connect('EnergyConsumption.db')
    cur = conn.cursor()

    # execute query to get data
    cur.execute('SELECT * FROM ElectricityConsumption;')
    data_fetched = cur.fetchall()
    conn.commit()

    # represent query result as json, then convert to list
    json_object = json.dumps(data_fetched, sort_keys = True)

    return json_object

# set up route for front end to get LBNL gas data from the database
@app.route('/gas_data')
def get_gas_data():
    # form connection to database
    conn = sqlite3.connect('EnergyConsumption.db')
    cur = conn.cursor()

    # execute query to get data
    cur.execute('SELECT Timestamp, THERMS FROM GasConsumption;')
    data_fetched = cur.fetchall()
    conn.commit()

    # represent query result as json, then convert to list
    json_object = json.dumps(data_fetched, sort_keys = True)

    return json_object

# set up route to get electricity forecast data and send it to the front end
@app.route('/electricity_forecast')
def make_forecast():
    # get electricity consumption forecast data from csv file
    electricity_consumption_forecast = pd.read_csv("data/ElectricityTimeSeriesForecast.csv")
    electricity_consumption_forecast = electricity_consumption_forecast[electricity_consumption_forecast['ElectricityConsumptionForecast'] != -1000]

    # convert the data to json format and return it to the front end
    return electricity_consumption_forecast.to_json(orient="index")

if __name__ == "__main__":
    app.run()
