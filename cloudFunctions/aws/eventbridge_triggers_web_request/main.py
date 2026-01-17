import httpx


def main(event: dict, context: dict) -> dict:
    """Main function to handle the event from the EventBridge.

    Args:
        event (dict): The event from the EventBridge.
        context (dict): The context from the EventBridge.

    Returns:
        dict: The response from the EventBridge.
    """
    print(event)
    print(context)
    return {"statusCode": 200, "body": "Hello, World!"}


if __name__ == "__main__":
    main(event={}, context={})
