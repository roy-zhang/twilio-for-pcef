from twilio.rest import Client
import csv
import utils

def block_then_txt(row):
    message = config["initial_message_hello"] + " " + row[0] + " " + config["initial_message_after_hello"]
    input("press enter to text\n" + message + "\n  to " + row[1])
    utils.log(config["sent_logs_filename"], "sent " + message + " to " + row[1])
    utils.txt(config["number_to_send_from"], client, row[1], "hello " + row[0] + " plz vote citizen")

def map_csv(csv_filename, map_row_fn):
    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            map_row_fn(row)

# start
config = utils.get_config()

client = Client(config["account"], config["token"])

map_csv(config["csv_filename"], block_then_txt)