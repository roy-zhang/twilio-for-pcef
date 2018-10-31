from twilio.rest import Client
import utils

config = utils.get_config()

client = Client(config["account"], config["token"])

def count_inbound(all_messages):
    return len([message for message in all_messages if message.direction == "inbound"])

def get_messages(client):
    all_messages = client.messages.list()
    print('There are {} messages in your account.'.format(count_inbound(all_messages)))
    for message in all_messages:
        if message.direction == "inbound":
            print("got " + message.body + " from " + message.from_ )
            utils.log(config["received_logs_filename"], "got " + message.body + " from " + message.from_)
            response = input("type response: ")
            if response != "skip":
                if response:
                    utils.txt(config["number_to_send_from"], client, message.from_, response)
                    utils.log(config["sent_logs_filename"], "sent " + response + " to " + message.from_)
                utils.delete_message(client, message.sid)

print("to delete and not respond, hit enter")
print("to skip and not delete, type \"skip\" then press enter")
get_messages(client)

print("no more new messages!")