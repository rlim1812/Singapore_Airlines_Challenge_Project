# import necessary packages
import sqlite3
import pandas as pd

# form connection to database
conn = sqlite3.connect('EnergyConsumption.db')
cur = conn.cursor()

# read in LBNL electricity consumption data and store it in the database
electricity_data = pd.read_excel('data/lbnl_building_74_electricity_data.xlsx')
electricity_data.to_sql('ElectricityConsumption', conn, index = False)

# read in LBNL gas consumption data and store it in the database
gas_data = pd.read_excel('data/lbnl_building_74_gas_data.xlsx')
gas_data.to_sql('GasConsumption', conn, index = False)

conn.commit()
