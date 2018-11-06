from twilio.rest import Client
import utils
import text_filter
import datetime
import sys

config = utils.get_config()

client = Client(config["account"], config["token"])

def number_to_message_list(messages):
    returnMe = {}
    for message in messages:
        if returnMe.get(message.from_, False):
            returnMe[message.from_].append(message)
        else:
            returnMe[message.from_] = [message]
    return returnMe

def count_inbound(all_messages):
    return len([message for message in all_messages if message.direction == "inbound"])

def format_date(date_str):
    return date_str.astimezone().strftime("%Y-%m-%d %I:%M %p")

def print_preamble(msgs):
    print("_________________________________________________________________\n"
          f"From {msgs[-1].from_}: @ {format_date(msgs[-1].date_sent)}\n"
          f"----------------------------------------\n\n"
          f"{body_of(msgs)}\n\n----------------------------------------")

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

def auto_respond(twilio_client, msgs, response_str):
    print(f"\n> autoresponding TO {msgs[-1].from_} <\n{body_of(msgs)}\n")
    txt_back(twilio_client, msgs, response_str)

def txt_back(twilio_client, msgs, reply_str):
    print(f"\n> SENDING TO {msgs[-1].from_} <\n{reply_str}\n"
          "_________________________________________________________________\n\n")
    try:
        delete_msg(twilio_client, msgs)
        utils.txt(msgs[-1].to, client, msgs[-1].from_, reply_str)
        utils.log(config["sent_logs_filename"], "sent " + reply_str + " to " + msgs[-1].from_)
    except Exception:
        print("skipping instead of deleting")

def delete_msg(twilio_client, msgs):
    for msg in msgs:
        utils.delete_message(twilio_client, msg.sid)
    print(f"> DELETING MESSAGE {body_of(msgs)}<\n " 
          "_________________________________________________________________\n\n")

def try_delete_msg(twilio_client, msgs):
    try:
        delete_msg(twilio_client, msgs)
    except Exception:
        print("skipping instead of deleting")

def body_of(msgs):
    return " ".join(reversed([msg.body for msg in msgs]))

def handle_message(twilio_client, msgs):
    body = body_of(msgs)
    if text_filter.has_wrong_number(body):
        if text_filter.has_already_voted(body):
            auto_respond(twilio_client, msgs, "Sorry! Thanks for voting anyways!")
        else:
            auto_respond(twilio_client, msgs, "Sorry! Hope you vote anyways!")
    elif text_filter.has_already_voted(body):
        auto_respond(twilio_client, msgs, "Great! Thanks for voting!")
    elif text_filter.has_stop_text(body) or text_filter.has_swear_words(body):
        print(f"> AUTODELETING MESSAGE {body}<\n "
              "_________________________________________________________________\n\n")
        try_delete_msg(twilio_client, msgs)
    else:
        print_preamble(msgs)
        utils.log(config["received_logs_filename"], "got " + body + " from " + msgs[-1].from_)
        response_selection = get_input()
        if response_selection == 'd':
            try_delete_msg(twilio_client, msgs)
        elif response_selection in ['1', '2', '3']:
            txt_back(twilio_client, msgs, config['canned_responses'][response_selection])
        elif response_selection == 's' or response_selection == '':
            print("> SKIPPING MESSAGE <\n"
                  "_________________________________________________________________\n\n")
        elif response_selection == 'q':
            print('Exiting.')
            sys.exit()
        else:
            txt_back(twilio_client, msgs, response_selection)

def get_messages(twilio_client):
    retrieved_messages = twilio_client.messages.list(limit=10000)
    filtered_messages = filter_numbers(retrieved_messages, config["last_number_floor"], config["last_number_ceiling"])
    print('\nThere are {} inbound messages in your account ...\n'.format(count_inbound(filtered_messages)))

    number_msg_map = number_to_message_list(filtered_messages)
    for number, message_list in number_msg_map.items():
        handle_message(client, message_list)


get_messages(client)

print("No more new messages!")
