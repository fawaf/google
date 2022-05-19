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
# authenticated user's account.
APIS = {
    "scopes": [
        "https://www.googleapis.com/auth/youtube",
        "https://www.googleapis.com/auth/siteverification",
        "https://www.googleapis.com/auth/admin.directory.domain",
        "https://www.googleapis.com/auth/admin.directory.group.member",
        "https://www.googleapis.com/auth/admin.directory.group",
        "https://www.googleapis.com/auth/admin.directory.user",
        "https://www.googleapis.com/auth/admin.directory.user.alias",
    ],
    "services": {
        "youtube": {
            "service_name": "youtube",
            "version": "v3",
        },
        "workspace": {
            "service_name": "admin",
            "version": "directory_v1",
        },
        "site_verification": {
            "service_name": "siteVerification",
            "version": "v1",
        },
    },
}


def get_credentials(api_name, client_secrets_file):
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, APIS["scopes"]
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


def get_and_update_credentials(
    client_secrets_filename, creds_filename, name, api_name
):
    credentials = get_credentials(
        api_name, client_secrets_file=client_secrets_filename
    )
    update_creds_file(creds_filename, name, credentials)

    return credentials


def load_credentials(
    api_name,
    creds_filename=CREDS_FILE,
    client_secrets_filename=CLIENT_SECRETS_FILE,
    name="default",
):
    creds_path = (
        f"{os.path.dirname(os.path.realpath(__file__))}/{creds_filename}"
    )
    if os.path.exists(creds_path):
        creds_file = open(creds_path, "r")
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
                    scopes=APIS["scopes"],
                )
            else:
                credentials = get_and_update_credentials(
                    client_secrets_filename, creds_path, name, api_name
                )
        except json.decoder.JSONDecodeError as e:
            print(e)

            credentials = get_and_update_credentials(
                client_secrets_filename, creds_path, name, api_name
            )
    else:
        credentials = get_and_update_credentials(
            client_secrets_filename, creds_path, name, api_name
        )

    return credentials


def get_client(name, api_name, client_secrets_filename=CLIENT_SECRETS_FILE):
    print(f"getting {api_name} client for {name}")

    creds = load_credentials(
        api_name, client_secrets_filename=client_secrets_filename, name=name
    )

    return googleapiclient.discovery.build(
        APIS["services"][api_name]["service_name"],
        APIS["services"][api_name]["version"],
        credentials=creds,
    )
