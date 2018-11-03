from twilio.rest import Client
import utils
import datetime

config = utils.get_config()

client = Client(config["account"], config["token"])

def count_inbound(all_messages):
    return len([message for message in all_messages if message.direction == "inbound"])

def print_preamble(message):
    print(f"From {message.from_}:\n--------------------------\n\n"
          f"{message.body}\n\n--------------------------\n")

def get_input():
    return input("To skip this message press enter.\n"
                 "To delete this message type 'd' and press enter.\n"
                 "Otherwise, type a response and press enter to send: ")

def between(numberStr, floor, ceiling):
    lastNumber = int(numberStr[-1:])
    return lastNumber >= floor and lastNumber <= ceiling

def filter_numbers(messages, floor, ceiling):
    return [message for message in messages if between(message.from_, floor, ceiling) and message.direction == "inbound"]

def time_what_hours_ago(hours_ago):
    return datetime.datetime.now() - datetime.timedelta(hours=hours_ago)

def get_messages(client):
    retrieved_messages = client.messages.list(limit=1000)
    filtered_messages = filter_numbers(retrieved_messages, config["last_number_floor"], config["last_number_ceiling"])
    print('There are {} inbound messages in your account ...\n'.format(count_inbound(filtered_messages)))
    for message in filtered_messages:
        if message.direction == "inbound":
            print_preamble(message)
            utils.log(config["received_logs_filename"], "got " + message.body + " from " + message.from_)
            response = get_input()
            if response.lower() == 'd':
                utils.delete_message(client, message.sid)
                print(">")
            elif response:
                print(f"\nSent {response} to {message.from_}.\n")
                utils.txt(message.to, client, message.from_, response)
                utils.log(config["sent_logs_filename"], "sent " + response + " to " + message.from_)
                utils.delete_message(client, message.sid)
                print(">")
            else:
                print(">")
                continue

get_messages(client)

print("No more new messages!")