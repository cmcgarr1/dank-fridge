import dropbox
import os
import sys
import datetime

def move_file(file_path,file_name):
    delete_folder='/home/pi/git/dank-fridge/files_to_delete'
    destination_path=os.path.join(delete_folder,file_name)
    try:
        os.rename(file_path,destination_path);
        print("file "+file_name+" moved")
    except:
        pass
def loop_drop_box(local_path, dropbox_path,dbx):
    with open(local_path, 'rb') as f:
        #dbx.put_file(dropbox_path, f)
        dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode('overwrite'))


def main():
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
            # construct the full local path
            local_path = os.path.join(root, filename)

            # construct the full Dropbox path
            relative_path = os.path.relpath(local_path,home_directory)

            dropbox_path = os.path.join(dropBox_directory, relative_path)

            # upload the file
            if os.path.isfile(local_path):
                print(filename)
                loop_drop_box(local_path,dropbox_path,dbx)
                move_file(local_path,filename)

    print('complete')

if __name__ == '__main__':
    main()



