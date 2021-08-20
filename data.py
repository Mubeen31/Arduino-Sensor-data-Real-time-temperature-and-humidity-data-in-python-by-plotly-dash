import pandas as pd
import serial
import csv
from datetime import datetime
import MySQLdb as mysql

# copy the port from your Arduino editor
PORT = 'COM5'
ser = serial.Serial(PORT, 9600)

humArray = []
tempArray = []
timeArray = []

while True:
        message = ser.readline()
        data = message.strip().decode()
        split_string = data.split(',')  # split string
        humidity = float(split_string[0])  # convert first part of string into float
        temperature = float(split_string[1])  # convert second part of string into float
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        # print(temperature)
        print(dt_string, humidity, temperature)
        humArray.append(humidity)  # add humidity values into array
        tempArray.append(temperature)  # add temperature values into array
        timeArray.append(dt_string)
        # print(humArray)
        # print(tempArray)
        # print(timeArray)
        with open("humidity_and_temperature.csv", "a") as f:
            writer = csv.writer(f, delimiter = ",")
            # writer.writerow(['Time', 'Humidity', 'Temperature'])
            writer.writerow([dt_string, humidity, temperature])

        # df = pd.DataFrame({'Time': timeArray, 'Humidity': humArray, 'Temperature': tempArray})
        # # print(df)

        # df.to_csv('humidity_and_temperature.csv', mode='a', header=False)
        # df1 = pd.read_csv('humidity_and_temperature.csv')
        # print(df1)

        # header_list = ['Time', 'Humidity', 'Temperature']
        # df1 = pd.read_csv('humidity_and_temperature.csv', names = header_list)
        # print(df1['Temperature'].iloc[-1])

        # Add data in mysql database
        # header_list = ['Time', 'Humidity', 'Temperature']
        # data = pd.read_csv('humidity_and_temperature.csv', names = header_list)
        # First create name of database in MySQL workbench 'humidity_and_temperature'
        # conn = mysql.connect(host = 'localhost',
        #                      database = 'humidity_and_temperature',
        #                      user = 'root',
        #                      password = 'sql_root_45t6')
        # cursor = conn.cursor()
        #
        # # Drop table if pollution name table exists in the database
        # cursor.execute('DROP TABLE IF EXISTS HumidityTemperature;')
        #
        # # Create statement for a table
        # cursor.execute('CREATE TABLE HumidityTemperature (Time DATETIME, '
        #                'Humidity FLOAT, '
        #                'Temperature FLOAT) '
        #                )
        # # Add the data of csv file into sql table
        # for row in data.itertuples():  # itertuples() function is used to iterate tuple rows
        #     cursor.execute('''
        #                 INSERT INTO HumidityTemperature (Time, Humidity, Temperature)
        #                 VALUES (%s,%s,%s)
        #                 ''',
        #                    (row.Time,
        #                     row.Humidity,
        #                     row.Temperature,
        #                     ))
        #
        #     # print('Records are adding into table ..........')
        #     conn.commit()