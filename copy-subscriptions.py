#!/usr/bin/env python

# This code sample shows how to get a channel subscription.
# python get_subscription.py --channel-id=UC_x5XG1OV2P6uZZ5FSM9Ttw

import sys
import json
import argparse

import googleapiclient.discovery
import googleapiclient.errors
import google_auth_oauthlib.flow
import google.auth

import utils


parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--from",
    type=str,
    dest="from_account",
    required=True,
    help="from account",
)
parser.add_argument("-t", "--to", type=str, required=True, help="to account")
args = parser.parse_args()

from_account = args.from_account
to = args.to

credentials = utils.load_credentials(
    client_secrets_filename="{}.json".format(from_account), name=from_account
)
to_credentials = utils.load_credentials(
    client_secrets_filename="{}.json".format(to), name=to
)

youtube = googleapiclient.discovery.build(
    utils.API_SERVICE_NAME, utils.API_VERSION, credentials=credentials
)
to_youtube = googleapiclient.discovery.build(
    utils.API_SERVICE_NAME, utils.API_VERSION, credentials=to_credentials
)

subscriptions = youtube.subscriptions()
to_subscriptions = to_youtube.subscriptions()

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
        utils.divider(char="-")
        print("description: {}".format(description))
        utils.divider(char="-")
        print(
            "channel url: https://www.youtube.com/channel/{}/videos".format(
                channel_id
            )
        )

        utils.divider(times=33)

        print("subscribing to {} on {}".format(channel_id, to))
        body = {
            "snippet": {
                "resourceId": {
                    "kind": "youtube#channel",
                    "channelId": channel_id,
                }
            }
        }
        try:
            sub_request = to_subscriptions.insert(part="snippet", body=body)
            response = sub_request.execute()
        except googleapiclient.errors.HttpError as e:
            print(e)

        utils.divider()

    request = subscriptions.list_next(request, subscriptions_list)
