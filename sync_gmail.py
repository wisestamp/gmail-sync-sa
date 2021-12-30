import requests
import sys
import json
from os.path import exists

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.settings.basic']
SERVICE_ACCOUNT_FILE = 'service_account.json'

MAX_USERS = 10

def sync_gmail(admin_email, domain, page_token=None):
    print('Updating gmail signatures for {} on behalf of {}'.format(domain, admin_email))
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    credentials = credentials.with_subject(admin_email)
    service = build('admin', 'directory_v1', credentials=credentials)
    results = service.users().list(maxResults=MAX_USERS, domain=domain, orderBy='email', pageToken=page_token).execute()

    users = results.get('users', [])
    next_page_token = results.get('nextPageToken', None)

    for user in users:
        try:
            signature_html = get_signature(user['primaryEmail'])
            update_gmail_signature(user['primaryEmail'], signature_html)
            print("updated user: {}".format(user['primaryEmail']))
        except:
            print("error updating user: {}".format(user['primaryEmail']))

    if next_page_token:
        sync_gmail(admin_email, domain, next_page_token)

def get_signature(email):
    res = requests.get("https://gapp.wisestamp.com/domain/user/view_signature/raw?email={}".format(email))
    return str(res.content, 'UTF-8')

def update_gmail_signature(email, signature_html):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=GMAIL_SCOPES)
    credentials = credentials.with_subject(email)
    service = build('gmail', 'v1', credentials=credentials)
    return service.users().settings().sendAs().patch(userId='me', sendAsEmail=email, body={"signature": signature_html}).execute()


if __name__ == '__main__':
    domain = ''
    admin_email = ''
    
    # Try to read config from config.json
    if exists('config.json'):
        config = json.load(open('config.json'))
        domain = config.get('domain')
        admin_email = config.get('admin_email')

    if not domain or not admin_email:
        print("Can't determine domain or/and admin email")
        sys.exit()
    
    sync_gmail(admin_email, domain)