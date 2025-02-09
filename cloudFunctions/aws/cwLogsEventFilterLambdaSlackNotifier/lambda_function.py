import json
import base64
import gzip
from boto3 import client

from slack_notifier import slack_notifier
from event_data import error_main

sm = client(service_name="secretsmanager")


def lambda_handler(event, context):

    print(event)
    log = event["awslogs"]["data"]
    log_data_compressed = base64.b64decode(log)
    log_data_decompressed = gzip.decompress(log_data_compressed)
    log_data_str = log_data_decompressed.decode("utf-8")

    error_logs = json.loads(log_data_str)
    print(error_logs)
    error_message = error_main(error_logs=error_logs)
    print(error_message)
    slack_notifier(error_message)
