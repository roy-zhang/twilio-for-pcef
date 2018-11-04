from twilio.rest import Client
import utils
import text_filter
import datetime
import sys

config = utils.get_config()

client = Client(config["account"], config["token"])

def count_inbound(all_messages):
    return len([message for message in all_messages if message.direction == "inbound"])

def format_date(date_str):
    return date_str.astimezone().strftime("%Y-%m-%d %I:%M %p")

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
          f"\t 's' - Skip this message.\n"
          f"\t 'd' - Delete this message.\n"
          f"\t 'q' - Quit the program.\n>> "
          f"\t     - or your own custom response\n", end='')
    return input()

def between(numberStr, floor, ceiling):
    lastNumber = int(numberStr[-1:])
    return floor <= lastNumber <= ceiling

def filter_numbers(messages, floor, ceiling):
    return [message for message in messages if between(message.from_, floor, ceiling) and message.direction == "inbound"]

def time_what_hours_ago(hours_ago):
    return datetime.datetime.now() - datetime.timedelta(hours=hours_ago)

def print_autoresponding(message):
    print(f"\n> autoresponding TO {message.from_} <\n{message.body}\n")

def txt_back(message, replyStr):
    print(f"\n> SENDING TO {message.from_} <\n{replyStr}\n"
          "_________________________________________________________________\n\n")
    utils.delete_message(client, message.sid)
    utils.txt(message.to, client, message.from_, replyStr)
    utils.log(config["sent_logs_filename"], "sent " + replyStr + " to " + message.from_)

def delete_msg(twilio_client, message):
    utils.delete_message(twilio_client, message.sid)
    print(f"> DELETING MESSAGE {message.body}<\n " 
          "_________________________________________________________________\n\n")

def get_messages(twilio_client):
    retrieved_messages = twilio_client.messages.list(limit=5000)
    filtered_messages = filter_numbers(retrieved_messages, config["last_number_floor"], config["last_number_ceiling"])
    print('\nThere are {} inbound messages in your account ...\n'.format(count_inbound(filtered_messages)))
    for message in filtered_messages:
        if text_filter.has_wrong_number(message.body):
            if text_filter.has_already_voted(message.body):
                print_autoresponding(message)
                txt_back(message, "Sorry! Thanks for voting anyways!")
            else:
                print_autoresponding(message)
                txt_back(message, "Sorry! Hope you vote anyways!")
        elif text_filter.has_already_voted(message.body):
            print_autoresponding(message)
            txt_back(message, "Great! Thanks for voting!")
        elif text_filter.has_stop_text(message.body) or text_filter.has_swear_words(message.body):
            print_autoresponding(message)
            delete_msg(twilio_client, message)
        else:
            print_preamble(message)
            utils.log(config["received_logs_filename"], "got " + message.body + " from " + message.from_)
            response_selection = get_input()
            if response_selection == 'd':
                delete_msg(twilio_client, message)
            elif response_selection in ['1', '2', '3']:
                txt_back(message, config['canned_responses'][response_selection])
            elif response_selection == 's' or response_selection == '':
                print("> SKIPPING MESSAGE <\n"
                      "_________________________________________________________________\n\n")
            elif response_selection == 'q':
                print('Exiting.')
                sys.exit()
            else:
                txt_back(message, response_selection)



get_messages(client)

print("No more new messages!")
