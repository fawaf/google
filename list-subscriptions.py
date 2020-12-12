#!/usr/bin/env python

# This code sample shows how to get a channel subscription.
# python get_subscription.py --channel-id=UC_x5XG1OV2P6uZZ5FSM9Ttw

import sys

import googleapiclient.discovery
import googleapiclient.errors
import google_auth_oauthlib.flow
import utils


if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = "test"

    credentials = utils.load_credentials(
        client_secrets_filename="{}.json".format(name), name=name
    )

    youtube = googleapiclient.discovery.build(
        utils.API_SERVICE_NAME, utils.API_VERSION, credentials=credentials
    )

    subscriptions = youtube.subscriptions()

    request = subscriptions.list(
        part="snippet", mine=True, order="alphabetical"
    )
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

            utils.divider()

        request = subscriptions.list_next(request, subscriptions_list)
