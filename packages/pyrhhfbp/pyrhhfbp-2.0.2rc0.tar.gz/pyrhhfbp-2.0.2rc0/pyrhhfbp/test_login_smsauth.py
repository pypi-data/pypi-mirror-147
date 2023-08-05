import json
import os
from typing import Dict
from pyrhhfbp import Robinhood


def get_robinhood_login_json(path='~/.robinhood/login.json') -> Dict:
    with open(os.path.abspath(os.path.expanduser(path))) as fh:
        obj = json.load(fh)
    return obj


if __name__ == '__main__':
    creds = get_robinhood_login_json()
    rh = Robinhood(username=creds['email'], password=creds['password'], challenge_type='sms')
    del creds

    print("rh.oauth.is_valid={}".format(rh.oauth.is_valid))
    if not rh.oauth.is_valid:
        print("logging in again.")
        rh.login()

    print("AAPL price:")
    rh.print_quote("AAPL")
