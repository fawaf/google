#!/usr/bin/env python

# This code sample shows how to get a channel subscription.
# python get_subscription.py --channel-id=UC_x5XG1OV2P6uZZ5FSM9Ttw

import argparse
import os
import re
import json

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
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
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

if __name__ == "__main__":
    youtube = get_authenticated_service()

    subscriptions = youtube.subscriptions()
    request = subscriptions.list(part="snippet", mine=True)
    while request is not None:
        subscriptions_list = request.execute()
        for subscription in subscriptions_list["items"]:
            sid = subscription["id"]

            snippet = subscription["snippet"]
            title = snippet["title"]
            description = snippet["description"]
            channel_id = snippet["channelId"]

            print("title: {}".format(title))
            print("description: {}".format(description))
            print("channel url: {}".format(channel_id))

            yn = input("Do you want to delete this subscription? ")
            r = re.compile('[Y|y][E|e][S|s]')
            if r.match(yn):
                subscriptions.delete(sid)

                print("subscription to {} was deleted.".format(title))
            else:
                print("skipping {}".format(title))

            print("=" * 44)

        request = subscriptions.list_next(request, subscriptions_list)
