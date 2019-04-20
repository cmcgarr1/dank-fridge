from __future__ import print_function
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
import Adafruit_DHT
import time


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)) ) # fastest
    return str(len(str_list)+1)

def convert_to_f(c_reading):
    f_reading=9/5.0*c_reading+32
    return f_reading

def get_temp():
    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)

    # Un-comment the line below to convert the temperature to Fahrenheit.
    # temperature = temperature * 9/5.0 + 32

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
    sleep_freq=300
    worksheet = None

    print('Logging sensor measurements')
    print('Press Ctrl-C to quit.')

    while True:
        if worksheet is None:
            #sheet = client.open("fridge temp").sheet1
            worksheet = login_open_sheet()

        atmo_data=get_temp()

        temp=convert_to_f(atmo_data[1])
        humd=atmo_data[0]

        print('Temperature: {0:0.1f} C'.format(temp))
        print('Humidity:    {0:0.1f} %'.format(humd))

        if humd is None or temp is None:
            time.sleep(2)
            continue

        try:
            next_row = next_available_row(worksheet)
            worksheet.update_cell(next_row,1, str(datetime.datetime.now()))
            worksheet.update_cell(next_row,2, str(temp))
            worksheet.update_cell(next_row,3, str(humd))
            #worksheet.append_row((datetime.datetime.now(), temp, humd))
        except:
            # Error appending data, most likely because credentials are stale.
            # Null out the worksheet so a login is performed at the top of the loop.
            print('Append error, logging in again')
            worksheet = None
            time.sleep(sleep_freq)
            continue

        print('test')
        time.sleep=(sleep_freq)


if __name__ == '__main__':
    main()
