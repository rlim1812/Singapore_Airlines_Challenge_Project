# import necessary packages
from flask import Flask
import simplejson as json
import sqlite3
import pandas as pd

# create Flask app
app = Flask(__name__)

# form connection to database
conn = sqlite3.connect('EnergyConsumption.db')
cur = conn.cursor()

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
