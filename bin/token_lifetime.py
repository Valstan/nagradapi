import time


def token_lifetime(token_date):
    difference = int(time.time()) - token_date
    if difference < 7777000:
        return True
