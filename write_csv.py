from __future__ import print_function
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
import Adafruit_DHT
import time
import csv
import os

def write_to_csv(fridge_data):
    cwd = '/home/pi/git/dank-fridge/temp_data_csv'
    current_time=datetime.datetime.now()
    file_name=cwd+'/dank_fridge_'+str(current_time.year)+'_'+str(current_time.month)+'_'+str(current_time.day)+'.csv'
    print(file_name)
    with open(file_name, 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(fridge_data)

def convert_to_f(c_reading):
    f_reading=9/5.0*c_reading+32
    return f_reading

def get_temp():
    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)

    # Un-comment the line below to convert the temperature to Fahrenheit.
    temperature = temperature * 9/5.0 + 32

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)
    return humidity, temperature

def login_open_sheet():
    try:
        scope =  [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        gc = gspread.authorize(credentials)
        worksheet = gc.open("fridge temp").sheet1
        return worksheet
    except Exception as ex:
        print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)

def main():
    temp_data=get_temp()
    output_temp_value=[[str(datetime.datetime.now()),str(temp_data[0]),str(temp_data[1])]]
    print(output_temp_value)
    write_to_csv(output_temp_value)

if __name__ == '__main__':
    main()
