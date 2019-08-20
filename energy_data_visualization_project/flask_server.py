# import necessary packages
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from flask import send_from_directory
import simplejson as json
import sqlite3
from dateutil import parser
from pmdarima.arima import auto_arima

# create Flask app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# form connection to database
conn = sqlite3.connect('EnergyConsumption.db')
cur = conn.cursor()

# Default web page
@app.route("/")
def index():
    return render_template("index.html")

# JSON_big = []

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
  
# set up route to make time series forecast and send data with prediction values to front end
@app.route('/make_forecast')
def make_forecast():
     return send_from_directory('data', "electricity_time_series_data_with_forecast.csv", as_attachment=True)

 if __name__ == "__main__":
    app.run(debug=True)
