import sqlite3
import pandas as pd
from dateutil import parser
from pmdarima.arima import auto_arima

# form connection to database
conn = sqlite3.connect('EnergyConsumption.db')
cur = conn.cursor()

# get data from database
electricity_data = pd.read_sql('SELECT * FROM ElectricityConsumption LIMIT 200;', con = conn)

# convert time column to datetime object type
time_values_datetime = []
time = electricity_data["Timestamp"]

i = 0
while i < len(time):
    time_value_datetime = parser.parse(time[i])
    time_values_datetime.append(time_value_datetime)
    i += 1

electricity_data["Timestamp"] = time_values_datetime
electricity_data_modified = electricity_data.set_index("Timestamp")

# Create ARIMA time series model
model = auto_arima(electricity_data_modified, start_p=1, start_q=1,
                                          max_p=20, max_q=20, m=12,
                                          start_P=0, seasonal=True,
                                              d=1, D=1, trace=True,
                                             error_action='ignore',
                                            suppress_warnings=True,
                                                     stepwise=True)

# Split the data into training data and testing data
training_data = electricity_data_modified.iloc[0:160,]
test_data =electricity_data_modified.iloc[160:,]

# fit the model to the training data
model.fit(training_data)

# make predictions using the model
forecast = model.predict(n_periods = 40)

# create a new dataframe that includes the electricity usage time series data and the forecast values
electricity_consumption_forecast = pd.DataFrame(forecast, index = test_data.index, columns = ["ElectricityConsumptionForecast"])
electricity_time_series_data_with_forecast = pd.concat([electricity_data, electricity_consumption_forecast], axis=1)
electricity_time_series_data_with_forecast.fillna(-1000, inplace = True)
energy_consumption_forecast_list = list(electricity_time_series_data_with_forecast["ElectricityConsumptionForecast"])

i = 200 - 1 - 39
j = 200

num_iterations = 40
for num_iter in range(num_iterations):
    temp = energy_consumption_forecast_list[i]
    energy_consumption_forecast_list[i] = energy_consumption_forecast_list[j]
    energy_consumption_forecast_list[j] = temp
    i += 1
    j += 1

electricity_time_series_data_with_forecast["ElectricityConsumptionForecast"] = energy_consumption_forecast_list
electricity_time_series_data_with_forecast = electricity_time_series_data_with_forecast.iloc[:200, :]

# store the dataframe as a table in sql database
# electricity_time_series_data_with_forecast.to_sql('ElectricityTimeSeriesForecast', conn, if_exists="replace", index = False)
electricity_time_series_data_with_forecast.to_csv("data/ElectricityTimeSeriesForecast.csv")

conn.commit()
