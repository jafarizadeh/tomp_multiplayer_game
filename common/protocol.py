import json


def parse_message(data):
    return json.load(data)

def make_message(msg_type, payload)
    return json.dump({
        "type" : msg_type,
        "payload" : payload,
    }) + "\n"

