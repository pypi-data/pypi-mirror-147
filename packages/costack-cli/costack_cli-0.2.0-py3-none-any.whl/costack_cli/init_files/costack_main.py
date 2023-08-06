import json

def handler(event, context):
    # get the params from the event, for example, user_name = event["user_name"]
    # note: if the handler is intended to be invoked as a API handler, the event will contain the meta information, see documentation for more information 
    return {
        "statusCode": 200,
        "body": "Welcome to costack!"
    }
