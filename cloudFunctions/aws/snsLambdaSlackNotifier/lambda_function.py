import slack_notifier
from sns_handling import sns_main


def lambda_handler(event, context):

    print(event)
    # --- For SNS notifications to slack ---
    sns_message = sns_main(event=event)
    slack_notifier.slack_notifier(sns_message)
