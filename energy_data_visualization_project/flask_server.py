# import necessary packages
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import simplejson as json
import sqlite3
import pandas as pdv
import pdb

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

    # import pdb; pdb.set_trace()

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

if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
