from __future__ import print_function
import datetime
import sys
import Adafruit_DHT
import csv

def write_to_csv(fridge_data):
    cwd = '/home/pi/git/dank-fridge/temp_data_csv'
    current_time=datetime.datetime.now()
    file_name=cwd+'/dank_fridge_'+str(current_time.year)+'_'+str(current_time.month)+'_'+str(current_time.day)+'.csv'
    with open(file_name, 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(fridge_data)

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

def main():
    temp_data=get_temp()
    output_temp_value=[[str(datetime.datetime.now()),str(temp_data[0]),str(temp_data[1])]]
    print(output_temp_value)
    write_to_csv(output_temp_value)

if __name__ == '__main__':
    main()
