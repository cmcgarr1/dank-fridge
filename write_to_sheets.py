from __future__ import print_function
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
import Adafruit_DHT
import csv
from googleapiclient import discovery

def read_csv_last_hour():
    current_time=datetime.datetime.now()
    current_time_millsec = current_time.timestamp() * 1000.0
    current_time_millsec_less_30=current_time_millsec-1800000.0
    current_time_less_30=datetime.datetime.fromtimestamp(current_time_millsec_less_30/1000.0)
    file_name='/home/pi/git/dank-fridge/temp_data_csv/dank_fridge_'+str(current_time_less_30.year)+'_'+str(current_time_less_30.month)+'_'+str(current_time_less_30.day)+'.csv'

    date_list=[]
    date_counter=0
    data_to_write=[]

    #with open(file_name, 'r',encoding='utf-8-sig') as readFile:
    with open(file_name, 'r') as readFile:
        reader = csv.reader(readFile,delimiter=',')
        lines = list(reader)

    for line in lines:
        date_converted=datetime.datetime.strptime(line[0],"%Y-%m-%d %H:%M:%S.%f")
        date_list.append(date_converted)

    for date_var in date_list:
        if date_var>=current_time_less_30 and date_var<current_time:
            data_to_write.append(lines[date_counter])
        date_counter+=1
    return data_to_write

def batch_upload_to_sheets(data_to_write,last_row,worksheet):
    range_str='Sheet1!A'+str(last_row)+':C'+str(last_row+len(data_to_write)-1)

    batch_update_values_request_body = {

    'value_input_option': 'USER_ENTERED',
    'data': [
        {
            "range": range_str,
            "majorDimension": "Rows",
            "values": data_to_write
        }
    ],
    }
    scope =  [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

    c1 = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/git/dank-fridge/client_secret.json', scope)
    service = discovery.build('sheets', 'v4', credentials=c1)

    request = service.spreadsheets().values().batchUpdate(spreadsheetId='1Quk4qrT2VyGcxN74_93RLET46WDju2DBVZTOpcdFaao', body=batch_update_values_request_body)
    #request = service.update_spreadsheet_value(spreadsheetId='1Quk4qrT2VyGcxN74_93RLET46WDju2DBVZTOpcdFaao', range_str, batch_update_values_request_body)
    response = request.execute()

   #         service.update_spreadsheet_value(spreadsheet_id, range, value_range_object, value_input_option: 'USER_ENTERED')

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)) ) # fastest
    return (len(str_list)+1)

def login_open_sheet():
    try:
        scope =  [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/git/dank-fridge/client_secret.json', scope)
        gc = gspread.authorize(credentials)
        worksheet = gc.open("fridge temp").sheet1
        return worksheet
    except Exception as ex:
        print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)

def main():

    data_to_write=read_csv_last_hour()

    worksheet = login_open_sheet()

    next_row=next_available_row(worksheet)

    batch_upload_to_sheets(data_to_write,next_row,worksheet)

    #worksheet.append_row((data_to_write))

if __name__ == '__main__':
    main()



