import json


def sns_notification_to_data(event: dict) -> dict:

    sns_data = {}

    actionable_info = event["Records"][0]["Sns"]["Message"]
    actionable_info = json.loads(actionable_info)

    sns_data["alarm_name"] = actionable_info["AlarmName"]
    sns_data["aws_account"] = actionable_info["AWSAccountId"]
    sns_data["alert_message"] = actionable_info["NewStateReason"]

    return sns_data


def sns_message_create(sns_data: dict) -> str:

    sns_message = f"""
===================================

AWS Account: {sns_data["aws_account"]}

Metric in alarm: {sns_data["alarm_name"]}

-----------------------------------

| ALERT |

{sns_data["alert_message"]}
"""

    print(sns_message)

    return sns_message


def sns_main(event) -> str:
    sns_data = sns_notification_to_data(event=event)
    sns_message = sns_message_create(sns_data=sns_data)

    return sns_message
