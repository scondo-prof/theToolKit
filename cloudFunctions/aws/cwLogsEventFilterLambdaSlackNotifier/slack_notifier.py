import random
import os
import requests
import boto3
import json


def slack_notifier(message):

    try:

        # This loads the value of the webhook payload url into the variable webhook by calling the secret_block variable

        sm = boto3.client("secretsmanager")
        webhook = sm.get_secret_value(SecretId=os.environ["WEBHOOK"])

        webhook = json.loads(webhook["SecretString"])

        print(webhook)

        # This is a list of icons that we have in our slack channel

        emoji_list = [
            ":catjam:",
            ":excuseme:",
            ":meow_party:",
            ":sonicdance_pbjtime:",
            ":typingcat:",
            ":snoop_pls:",
            ":sadpepe:",
            ":leo-toast:",
            ":10-4:",
            ":3178-pepe-suffering:",
            ":9947_wiseau:",
            ":759906233397674015:",
            ":get-out:",
            ":amusement:",
            ":baited:",
            ":good_jello:",
            ":hello:",
            ":scared_af:",
            ":slov-squat-pepe:",
            ":sus_squirrel:",
            ":wanted_chicken:",
            ":zoom_zoom:",
            ":zoom_zoom_zoom:",
            ":zoom_zoom_zoom_zoom:",
        ]

        value = random.randint(1, len(emoji_list) - 1)
        emoji = emoji_list[value]
        channel = os.environ["CHANNEL"]
        username = os.environ["USER"]

        payload = (
            "{'channel': '"
            + channel
            + "','username': '"
            + username
            + "','text': "
            + "'"
            + message
            + "'"
            + ",'icon_emoji': '"
            + emoji
            + "'}"
        )

        print(requests.post(webhook, payload))

    except Exception as error:

        print(error)
