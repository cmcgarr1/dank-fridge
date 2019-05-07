import dropbox
import os
import sys
import datetime

time_now=datetime.datetime.now()
dropBox_directory="/dank-fridge/"
home_directory="/home/pi/git/dank-fridge/temp_data_csv"

file1 = open("/home/pi/git/dank-fridge/dropbox_key.txt","r")
key_raw= file1.readlines()
key_dbx=key_raw[0].strip('\n')

dbx = dropbox.Dropbox(key_dbx)

print('starting upload')
print(str(time_now))

for root, dirs, files in os.walk(home_directory):

    for filename in files:
        print(filename)
        # construct the full local path
        local_path = os.path.join(root, filename)

        # construct the full Dropbox path
        relative_path = os.path.relpath(local_path,home_directory)

        dropbox_path = os.path.join(dropBox_directory, relative_path)

        # upload the file
        with open(local_path, 'rb') as f:
            #dbx.put_file(dropbox_path, f)
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite, autorename=True)



print('complete')
