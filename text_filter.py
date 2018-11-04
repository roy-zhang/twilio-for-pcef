import re

def has(regex, body):
    return bool(re.com)

def has_wrong_number(body):
    return bool(re.compile(r'(?i)^.*(wrong number|wrong #|wrong person|this isn\'t|this is not).*$').search(body))

def has_already_voted(body):
    return bool(re.compile(r'(?i)^.*(already voted|voted already).*$').search(body))
