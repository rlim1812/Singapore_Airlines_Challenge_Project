import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import mean_squared_error, r2_score

# form connection to database
conn = sqlite3.connect('EnergyConsumption.db')
cur = conn.cursor()

num_rows = 1000
# get data from database
time_series_data = pd.read_sql('SELECT * FROM ElectricityConsumption LIMIT {};'.format(num_rows), con = conn)
time_series_data = time_series_data.loc[:,["Timestamp", "Building 74 - kWh Total Electricity (kWh)"]]

# preprocess the data
energy_consumption_values_list = list(time_series_data["Building 74 - kWh Total Electricity (kWh)"])
previous_value_1_step_time_lag = []
previous_value_2_step_time_lag = []
previous_value_3_step_time_lag = []
previous_value_4_step_time_lag = []

i = 4
while i < len(energy_consumption_values_list):
    previous_value_1_step_time_lag.append(energy_consumption_values_list[i - 1])
    previous_value_2_step_time_lag.append(energy_consumption_values_list[i - 2])
    previous_value_3_step_time_lag.append(energy_consumption_values_list[i - 3])
    previous_value_4_step_time_lag.append(energy_consumption_values_list[i - 4])
    i += 1

time_series_data = time_series_data.iloc[4:,:]
time_series_data.insert(2, "1 Step Time Lag", previous_value_1_step_time_lag)
time_series_data.insert(3, "2 Step Time Lag", previous_value_2_step_time_lag)
time_series_data.insert(4, "3 Step Time Lag", previous_value_3_step_time_lag)
time_series_data.insert(5, "4 Step Time Lag", previous_value_4_step_time_lag)

# Split the data into training set and test set
X = time_series_data.iloc[:,2:6]
y = time_series_data.iloc[:,1]

cut_off_value = int(0.8 * time_series_data.shape[0])
X_train = X.iloc[0:cut_off_value,]
X_test = X.iloc[cut_off_value:,]
y_train = y.iloc[0:cut_off_value,]
y_test = y.iloc[cut_off_value:,]

# Build the model and perform predictions
ridge_regression_model = Ridge()
ridge_regression_model.fit(X_train, y_train)
y_pred = ridge_regression_model.predict(X_test)

prediction_values = [0 for i in range(time_series_data.shape[0])]

i = len(prediction_values) - 1
j = len(y_pred) - 1

while j >= 0:
    prediction_values[i] = y_pred[j]
    i -= 1
    j -= 1

time_series_data.insert(1, "Prediction", prediction_values)

# save the data as a csv file
time_series_data.to_csv("data/ElectricityTimeSeriesForecast.csv")

conn.commit()
