from twilio.rest import Client
import utils
import datetime
import sys

config = utils.get_config()

client = Client(config["account"], config["token"])

def count_inbound(all_messages):
    return len([message for message in all_messages if message.direction == "inbound"])

def format_date(dateStr):
    return dateStr.astimezone().strftime("%Y-%m-%d %I:%M %p")

def print_preamble(message):
    print("_________________________________________________________________\n"
          f"From {message.from_}: @ {format_date(message.date_sent)}\n"
          f"----------------------------------------\n\n"
          f"{message.body}\n\n----------------------------------------")

def get_input():
    print(f"Select your response:\n"
          f"\t '1' - {config['canned_responses']['1']}\n"
          f"\t '2' - {config['canned_responses']['2']}\n"
          f"\t '3' - {config['canned_responses']['3']}\n"
          f"\t '4' - Enter your own response.\n"
          f"\t 's' - Skip this message.\n"
          f"\t 'd' - Delete this message.\n"
          f"\t 'q' - Quit the program.\n>> ", end='')
    while True:
        r = input()
        if r in ['1', '2', '3', '4', 's', 'd', 'q']:
            return r
        else:
            print('(1, 2, 3, 4, s, d, or q) >> ', end='')
            continue

def between(numberStr, floor, ceiling):
    lastNumber = int(numberStr[-1:])
    return lastNumber >= floor and lastNumber <= ceiling

def filter_numbers(messages, floor, ceiling):
    return [message for message in messages if between(message.from_, floor, ceiling) and message.direction == "inbound"]

def time_what_hours_ago(hours_ago):
    return datetime.datetime.now() - datetime.timedelta(hours=hours_ago)

def get_messages(client):
    retrieved_messages = client.messages.list(limit=100)
    filtered_messages = filter_numbers(retrieved_messages, config["last_number_floor"], config["last_number_ceiling"])
    print('\nThere are {} inbound messages in your account ...\n'.format(count_inbound(filtered_messages)))
    for message in filtered_messages:
        if message.direction == "inbound":
            print_preamble(message)
            utils.log(config["received_logs_filename"], "got " + message.body + " from " + message.from_)
            response_selection = get_input()
            if response_selection == 'd':
                utils.delete_message(client, message.sid)
                print("> DELETING MESSAGE <\n"
                      "_________________________________________________________________\n\n")
            elif response_selection == '4':
                custom_response = input("ENTER CUSTOM RESPONSE:\n")
                print(f"\n> SENDING TO {message.from_} <\n{custom_response}\n"
                      "_________________________________________________________________\n\n")
                utils.txt(message.to, client, message.from_, custom_response)
                utils.log(config["sent_logs_filename"], "sent " + custom_response + " to " + message.from_)
                utils.delete_message(client, message.sid)
            elif response_selection in ['1', '2', '3']:
                print(f"\n> SENDING TO {message.from_} <\n{config['canned_responses'][response_selection]}\n"
                      "_________________________________________________________________\n\n")
                utils.txt(message.to, client, message.from_, custom_response)
                utils.log(config["sent_logs_filename"], "sent " + custom_response + " to " + message.from_)
                utils.delete_message(client, message.sid)
            elif response_selection == 's':
                print("> SKIPPING MESSAGE <\n"
                      "_________________________________________________________________\n\n")
            elif response_selection == 'q':
                print('Exiting.')
                sys.exit()


get_messages(client)

print("No more new messages!")
