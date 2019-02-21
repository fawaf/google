#!/usr/bin/env python

# This code sample shows how to get a channel subscription.
# python get_subscription.py --channel-id=UC_x5XG1OV2P6uZZ5FSM9Ttw

import os
import re
import json
import httplib2

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secret.json"
CREDS_FILE = "creds.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user"s account.
SCOPE = "https://www.googleapis.com/auth/youtube"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

secrets = json.loads(open(CLIENT_SECRETS_FILE).read())
client_id = secrets["client_id"]
client_secret = secrets["client_secret"]

flow = OAuth2WebServerFlow(client_id, client_secret, SCOPE)

def divider(char="=", times=65):
    print(char * times)

if __name__ == "__main__":
    storage = Storage(CREDS_FILE)

    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, tools.argparser.parse_args())

    http = httplib2.Http()
    http = credentials.authorize(http)

    youtube = build(API_SERVICE_NAME, API_VERSION, http=http)
    subscriptions = youtube.subscriptions()
    request = subscriptions.list(part="snippet", mine=True, order="alphabetical")
    while request is not None:
        subscriptions_list = request.execute()
        for subscription in subscriptions_list["items"]:
            sid = subscription["id"]

            snippet = subscription["snippet"]
            title = snippet["title"]
            description = snippet["description"]
            channel_id = snippet["resourceId"]["channelId"]

            print("title: {}".format(title))
            divider(char="-")
            print("description: {}".format(description))
            divider(char="-")
            print("channel url: https://www.youtube.com/channel/{}/videos".format(channel_id))
            print()
            print()

            print("deleting subscription... ", end="")
            try:
                subscriptions.delete(id=sid).execute()
            except HttpError as e:
                print("error: {}".format(e))
            print("done.")

            divider()

        request = subscriptions.list_next(request, subscriptions_list)
