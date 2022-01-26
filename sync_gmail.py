import requests
import sys
import json
from os.path import exists

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account


GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.settings.basic']

VERSION = "1.0"
WISESTAMP_HOST = "https://gapp.wisestamp.com"
GET_SIGNATURE_API = "/api/domain/get_signatures"


def sync_gmail(cursor="", num=1):
    wisestamp_users_data = get_wisestamp_data(cursor=cursor)
    cursor = wisestamp_users_data["cursor"]
    last_iteration = wisestamp_users_data["last_iteration"]
    for data in wisestamp_users_data["data"]:
        user_key = data["user_key"]
        signature = data["signature"]
        try:
            update_gmail_signature(user_key, signature)
            print("[{num}::{user_key}] Set signature successfully".format(num=num, user_key=user_key))
            num += 1
        except Exception as e:
            print("[{num}::{user_key}] Error {error}".format(num=num, user_key=user_key, error=e))
    if not last_iteration:
        sync_gmail(cursor=cursor, num=num)

   
def get_wisestamp_data(cursor=""):
    try:
        res = requests.get("{host}/{api}?token={token}&cursor={cursor}&version={version}".format(
            host=WISESTAMP_HOST, 
            api=GET_SIGNATURE_API, 
            token=SIGNATURE_TOKEN, 
            cursor=cursor,
            version=VERSION
            )
        )
        wisestamp_users_data = json.loads(str(res.content, 'UTF-8'))
        error_message = wisestamp_users_data.get("message")
        if error_message:
            print(error_message)
            sys.exit()
        elif not wisestamp_users_data.get("data"):
            print("Finished processing")
            sys.exit()
        return wisestamp_users_data
    except Exception as e:
        print("Error: status code {status_code}".format(status_code=res.status_code))
        sys.exit()


def update_gmail_signature(email, signature_html):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=GMAIL_SCOPES)
    credentials = credentials.with_subject(email)
    service = build('gmail', 'v1', credentials=credentials)
    return service.users().settings().sendAs().patch(userId='me', sendAsEmail=email, body={"signature": signature_html}).execute()


if __name__ == '__main__':
    if exists('config.json'):
        config = json.load(open('config.json'))
        SIGNATURE_TOKEN = config.get('SIGNATURE_TOKEN')
        SERVICE_ACCOUNT_FILE = config.get('SERVICE_ACCOUNT_FILE')
        if not SIGNATURE_TOKEN or not SERVICE_ACCOUNT_FILE:
            print("Can't determine SIGNATURE_TOKEN or/and SERVICE_ACCOUNT_FILE")
            sys.exit()
        sync_gmail()
    else:
        print("Can't find config.json")
