from cw_logs_data import cw_logs_sub_filter_set


def lambda_handler(event, context):
    print("Start Assessment")
    print("===")
    cw_logs_sub_filter_set()
    print("===")
    print("Finished Assessment")
