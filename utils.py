import json


def get_config():
    with open('config.json') as f:
        return json.load(f)

def log(log_filename, msg):
    fo = open(log_filename, "a")
    try:
        fo.write(msg + "\n")
    except UnicodeEncodeError:
        fo.write('This message had an emoji.\n')
    fo.close()

def txt(from_number, client, number, message):
    client.messages.create(to=number, from_=from_number, body=message)

def delete_message(client, message_sid):
    try:
        client.messages(message_sid).delete()
    except Exception:
        print("skipping instead of deleting")

