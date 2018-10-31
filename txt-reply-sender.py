from twilio.rest import Client
import utils

config = utils.get_config()

client = Client(config["account"], config["token"])

def get_messages(client):
    all_messages = client.messages.list()
    print('There are {} messages in your account.'.format(len(all_messages)))
    for message in all_messages:
        if message.direction == "inbound":
            print("got " + message.body + " from " + message.from_ )
            utils.log(config["received_logs_filename"], "got " + message.body + " from " + message.from_)
            response = input("type response: ")
            if response:
                utils.txt(client, message.from_, response)
                utils.delete_message(client, message.sid)
                utils.log(config["sent_logs_filename"], "sent " + response + " to " + message.from_)

get_messages(client)

print("no more new messages!")