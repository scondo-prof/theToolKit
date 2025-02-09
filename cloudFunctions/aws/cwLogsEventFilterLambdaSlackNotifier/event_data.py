import json
import datetime


def timestampToDateTime(timestamp: str) -> str:
    timestamp_seconds = timestamp / 1000.0

    datetime_object = datetime.datetime.fromtimestamp(timestamp_seconds)
    date_string = datetime_object.strftime("%Y-%m-%d %H:%M:%S")

    return date_string


def format_error_logs(error_logs: dict) -> dict:
    error_obj = {
        "account": error_logs["owner"],
        "logGroup": error_logs["logGroup"],
        "logStream": error_logs["logStream"],
    }
    errors = []

    for log in error_logs["logEvents"]:
        time = timestampToDateTime(log["timestamp"])
        message = log["message"].replace("/", "")
        message = message.replace("\\", "")
        message = message.replace("'", "")
        message = message.replace('"', "")
        message = message.replace("\xa0", "")

        time_log = {"time": time, "message": message}
        errors.append(time_log)
    error_obj["errorLogs"] = errors

    return error_obj


def create_error_message(error_obj: dict) -> str:
    error_message = f"""
=============

|Lambda Error|

Account: {error_obj['account']} 

Log Group: <{error_obj['logGroup']}>

Log Stream: <{error_obj['logStream']}>

---------------------------------------------
Logs:
    """
    for log in error_obj["errorLogs"]:
        print(log["message"])

        error_message += f"""
!
|Time|: {log['time']}

<Error>: {log['message']}

"""

    return error_message


def error_main(error_logs: dict) -> str:
    error_obj = format_error_logs(error_logs=error_logs)
    error_message = create_error_message(error_obj=error_obj)

    return error_message
