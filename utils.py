#!/usr/bin/env python

# This code sample shows how to get a channel subscription.
# python get_subscription.py --channel-id=UC_x5XG1OV2P6uZZ5FSM9Ttw

import re
import json
import os

import googleapiclient.discovery
import googleapiclient.errors
import google_auth_oauthlib.flow
import google.auth

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secret.json"
CREDS_FILE = "creds.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user"s account.
SCOPES = ["https://www.googleapis.com/auth/youtube"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


def divider(char="=", times=65):
    print(char * times)


def get_credentials(client_secrets_file):
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES
    )
    credentials = flow.run_local_server()

    return credentials


def update_creds_file(creds_filename, name, credentials):
    creds_dict = {}

    if os.path.exists(creds_filename):
        try:
            creds_file = open(creds_filename, "r")

            creds_dict = json.load(creds_file)
        except json.decoder.JSONDecodeError as e:
            print(e)

    creds_dict[name] = json.loads(credentials.to_json())

    f = open(creds_filename, "w")
    f.write(json.dumps(creds_dict))
    f.close()


def get_and_update_credentials(client_secrets_filename, creds_filename, name):
    credentials = get_credentials(client_secrets_file=client_secrets_filename)
    update_creds_file(creds_filename, name, credentials)

    return credentials


def load_credentials(
    creds_filename=CREDS_FILE,
    client_secrets_filename=CLIENT_SECRETS_FILE,
    name="default",
):
    if os.path.exists(creds_filename):
        creds_file = open(creds_filename, "r")
        full_creds_dict = {}

        try:
            full_creds_dict = json.load(creds_file)

            if name in full_creds_dict:
                creds_dict = full_creds_dict[name]

                credentials = google.oauth2.credentials.Credentials(
                    creds_dict["token"],
                    refresh_token=creds_dict["refresh_token"],
                    token_uri=creds_dict["token_uri"],
                    client_id=creds_dict["client_id"],
                    client_secret=creds_dict["client_secret"],
                    scopes=SCOPES,
                )
            else:
                credentials = get_and_update_credentials(
                    client_secrets_filename, creds_filename, name
                )
        except json.decoder.JSONDecodeError as e:
            print(e)

            credentials = get_and_update_credentials(
                client_secrets_filename, creds_filename, name
            )
    else:
        credentials = get_and_update_credentials(
            client_secrets_filename, creds_filename, name
        )

    return credentials
