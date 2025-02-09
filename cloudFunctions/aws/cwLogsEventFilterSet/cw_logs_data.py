import boto3
import os

client = boto3.client("logs")


def get_log_groups() -> list[str]:
    log_groups = client.describe_log_groups()
    log_group_names = []

    while "nextToken" in log_groups.keys():
        for group in log_groups["logGroups"]:
            if "lambda/" in group["logGroupName"]:
                log_group_names.append(group["logGroupName"])
        log_groups = client.describe_log_groups(nextToken=log_groups["nextToken"])

    for group in log_groups["logGroups"]:
        if "lambda/" in group["logGroupName"]:
            log_group_names.append(group["logGroupName"])

    return log_group_names


def get_log_filters(log_groups_names: list[str]) -> dict:
    log_groups = {}
    for group in log_groups_names:
        group_sub_filters = client.describe_subscription_filters(
            logGroupName=group,
        )
        if not group_sub_filters["subscriptionFilters"]:
            log_groups[group] = group_sub_filters

    print(log_groups)
    return log_groups


def add_subscripton_filters(log_groups: dict):
    print(f"=== {os.environ['LAMBDAARN']} ===")
    for group in log_groups:
        try:
            print(f"Applying error filter to : {group}")
            response = client.put_subscription_filter(
                logGroupName=group,
                filterName="lambda-error-filter",
                filterPattern="%ERROR%",
                destinationArn=os.environ["LAMBDAARN"],
            )
            print(response)
        except Exception as e:
            print(f"This went wrong while applying filter to: {group}")
            print(e)


def cw_logs_sub_filter_set():
    log_groups_names = get_log_groups()
    log_groups = get_log_filters(log_groups_names=log_groups_names)
    add_subscripton_filters(log_groups=log_groups)
