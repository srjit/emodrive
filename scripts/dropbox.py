#! /usr/bin/python

import dropbox

## testing upload dropbox

access_token="LADJrEFyvzAAAAAAAAAAPmxqPUmb_CQlDVK-iUvXLKyk6DbxuoV_0_UVoqTqZoIa"

dbx = dropbox.Dropbox(access_token)

## account information
dbx.users_get_current_account()


## get all files in dropbox
for entry in dbx.files_list_folder('').entries:
    print(entry.name)

file_name='/home/sree/code/emodrive/images/neutral.jpg'

upload_path="/images/neutral.jpg"
dbx=dropbox.Dropbox(access_token)

with open(file_name, 'rb') as f:
    dbx.files_upload(f.read(),upload_path,mute=True)
