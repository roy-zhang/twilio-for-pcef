from twilio.rest import Client
import utils

config = utils.get_config()

client = Client(config["account"], config["token"])

def count_inbound(all_messages):
    return len([message for message in all_messages if message.direction == "inbound"])

def get_messages(client):
    all_messages = client.messages.list()
    print('There are {} inbound messages in your account ...\n'.format(count_inbound(all_messages)))
    for message in all_messages:
        if message.direction == "inbound":
            print("<")
            print(f"From {message.from_}:\n--------------------------\n\n"
                  f"{message.body}\n\n--------------------------\n")
            utils.log(config["received_logs_filename"], "got " + message.body + " from " + message.from_)
            response = input("To skip this message press enter.\n"
                             "To delete this message type 'd' and press enter.\n"
                             "Otherwise, type a response and press enter to send: ")
            if response.lower() == 'd':
                utils.delete_message(client, message.sid)
                print(">")
            elif response:
                print(f"\nSent {response} to {message.from_}.\n") 
                utils.txt(config["number_to_send_from"], client, message.from_, response)
                utils.log(config["sent_logs_filename"], "sent " + response + " to " + message.from_)
                utils.delete_message(client, message.sid)
                print(">")
            else:
                print(">")
                continue

get_messages(client)

print("No more new messages!")