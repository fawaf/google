#!/usr/bin/env python

# This code sample shows how to get a channel subscription.
# python get_subscription.py --channel-id=UC_x5XG1OV2P6uZZ5FSM9Ttw

import argparse
import os
import re
import json

import google.oauth2.credentials as credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secret.json"
CREDS_FILE = "creds"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user"s account.
SCOPES = ["https://www.googleapis.com/auth/youtube"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def get_authenticated_service():
    if os.path.isfile(CREDS_FILE):
        creds = json.loads(open(CREDS_FILE))
        credentials = creds.Credentails(creds["token"])
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_console()
        creds = {
                    "token": credentials.id_token
                }

        creds_file = open(CREDS_FILE, "w")
        json.dump(creds, creds_file)

    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

# subscription to the specified channel.
def get_subscriptions(youtube):
    get_subscription_response = youtube.subscriptions().list(part="snippet", mine=True).execute()

    return get_subscription_response["items"]

if __name__ == "__main__":
    youtube = get_authenticated_service()

    try:
        subscriptions = get_subscriptions(youtube)
        for subscription in subscriptions:
            print("A subscription to {} was deleted.".format(subscription))
    except:
        print("An error {} occurred: {}".format(e.resp.status, e.content))
