import dropbox
import os
import sys

dbx = dropbox.Dropbox('')

for root, dirs, files in os.walk("/Users/emmettmcgarr/git_programs/dank-fridge/csvs"):

    for filename in files:

        # construct the full local path
        local_path = os.path.join(root, filename)

        # construct the full Dropbox path
        relative_path = os.path.relpath(local_path, "/Users/emmettmcgarr/git_programs/dank-fridge")
        print(relative_path)
        dropbox_path = os.path.join("/dank-fridge/", relative_path)

        # upload the file
        with open(local_path, 'rb') as f:
            #dbx.put_file(dropbox_path, f)
            dbx.files_upload(f.read(), dropbox_path)


