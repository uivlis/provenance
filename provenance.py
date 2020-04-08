import fire
import os
from dotenv import load_dotenv

load_dotenv()
auth = (os.getenv('ALETHIO_KEY'), '')

import requests

def prove(address, token):

    is_address = requests.get(
        'https://api.aleth.io/v1/accounts/' + hex(address),
        auth=auth
    ).status_code

    if is_address != requests.codes.ok:
        raise ValueError('Address provided is not valid.')

    is_token = requests.get(
        'https://api.aleth.io/v1/tokens/' + hex(token),
        auth=auth
    ).status_code
    
    if is_token != requests.codes.ok:
        raise ValueError('Token provided is not valid.')

    balance = requests.get(
        'https://api.aleth.io/v1/token-balances?filter[account]=' + hex(address) + '&filter[token]=' + hex(token),
        auth=auth
    ).json()['data'][0]['attributes']['balance']

    if balance == 0:
        raise ValueError('No balance of token at address provided.')

    to_address = requests.get(
        'https://api.aleth.io/v1/token-transfers?filter[to]=' + hex(address),
        auth=auth
    ).json()

    tokens_to_address = [tx for tx in to_address['data'] if tx['relationships']['token']['data']['id'] == hex(token)]

    originators = [requests.get('https://api.aleth.io/v1/token-transfers/' + tx['id'] + '/originator', auth=auth).json()['data']['id'] for tx in tokens_to_address]

    originators = [hex(0) if originator == hex(address) else originator for originator in originators]

    return originators

if __name__ == '__main__':
  fire.Fire()