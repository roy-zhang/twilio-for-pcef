import csv
import utils
import text_filter
import utils

def classify(msg):
    if text_filter.has_already_voted(msg):
        return "already voted"
    elif text_filter.has_just_stop(msg) or text_filter.has_stop_text(msg):
        return "stop"
    elif text_filter.has_swear_words(msg):
        return "swear words"
    elif text_filter.has_wrong_number(msg):
        return "wrong number"
    else:
        return ""

def if_match_then_print(row):
    number = row[11]
    if number in numberToMsg:
        msg = numberToMsg[number]
        utils.log(config["responses_filename"], str(",".join(row) + "," + msg + "," + classify(msg)))

def map_csv(csv_filename, map_row_fn):
    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            map_row_fn(row)

def number_to_msg(got_filename):
    returnMe = {}
    with open(got_filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            returnMe[row[1]] = row[0]
    return returnMe

if __name__ == '__main__':
    config = utils.get_config()

    numberToMsg = number_to_msg(config["got_filename"])

    print("got " + str(len(numberToMsg)))

    map_csv(config["full_van_filename"], if_match_then_print)
