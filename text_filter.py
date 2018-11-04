import re

def has(regex, body):
    return bool(re.com)

def has_wrong_number(body):
    return bool(re.compile(r'(?i)^.*(wrong number|wrong phone number|wrong #|wrong person|this isn\'t|this is not).*$').search(body))

def has_already_voted(body):
    return bool(re.compile(r'(?i)^.*(already voted|voted already|did vote|have voted|dropped off|mailed).*$').search(body))

def has_just_stop(body):
    return bool(re.compile(r'(?i)^stop$').search(body))

def has_stop_text(body):
    return has_just_stop(body) or bool(re.compile(r'(?i)^.*(do not text|don\'t text|take me off|stop text|unsubscribe).*$').search(body))

def has_swear_words(body):
    return bool(re.compile(r'(?i)^.*(fuck|shit|bitch|cunt|goddamn|biatch|crap|damn|prick|slut|whore).*$').search(body))
