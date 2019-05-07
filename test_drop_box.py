import dropbox
import os
import sys

file1 = open("/home/pi/git/dank-fridge/dropbox_key.txt","r")
key_raw= file1.readlines()
key_dbx=key_raw[0].strip('\n')

dbx = dropbox.Dropbox(key_dbx)


for root, dirs, files in os.walk("/home/pi/git/dank-fridge/test_delete_csv/temp_data_csv"):

    for filename in files:
        print(filename)
        # construct the full local path
        local_path = os.path.join(root, filename)

        # construct the full Dropbox path
        relative_path = os.path.relpath(local_path,"/home/pi/git/dank-fridge/test_delete_csv/temp_data_csv")

        dropbox_path = os.path.join("/dank-fridge/", relative_path)

        # upload the file
        with open(local_path, 'rb') as f:
            #dbx.put_file(dropbox_path, f)
           #first_line=f.read()
           dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode('overwrite'))
        #print(first_line)


