from twilio.rest import Client
import json
import csv


def get_config():
    with open('config.json') as f:
        return json.load(f)


def map_csv(csv_filename, map_row_fn):
    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            map_row_fn(row)


def call(number, message):
    client.messages.create(to="+1"+number, from_="+13195354205", body=message)


def call_row(row):
    call(row[1], "hello " + row[0])


def print_row(row):
    print(row[0], " | ", row[1])


def log(log_filename, msg):
    fo = open(log_filename, "a")
    fo.write(msg + "\n")
    fo.close()


def io_loop_forever(input_fn):
    while True:
        str = input("Enter your input: ");
        input_fn("Received input is : ", str)


def get_messages(client):
    all_messages = client.messages.list()
    print('There are {} messages in your account.'.format(len(all_messages)))
    for message in all_messages:
        print(message)

# start
config = get_config()
log(config["log_filename"], "starting the program")


client = Client(config["account"], config["token"])
map_csv(config["csv_filename"], print_row)

#map_csv(config["csv_filename"], call_row)


get_messages(client)



#get_messages(client)

#io_loop_forever(print)


#message = client.messages.create(to="+13194006347", from_="+13195354205",
#                                 body="Hello there!")
