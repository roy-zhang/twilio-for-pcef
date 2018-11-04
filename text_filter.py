import re


def is_wrong_number(body):
    return bool(re.compile(r'(?i)^.*(wrong number|wrong #|wrong person).*$').search(body))
