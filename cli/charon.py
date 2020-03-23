#!/usr/bin/env python3

import requests


def register_bot(charon_url: str, bot_token: str, signing_secret: str, bot_api_key: str, bot_url: str,
                 auth_code: str) -> bool:
    payload = {
        "bot_token": bot_token,
        "signing_secret": signing_secret,
        "bot_api_key": bot_api_key,
        "bot_url": bot_url,
        "authentication_code": auth_code
    }
    r = requests.post(f'{charon_url}/roman/registration', json=payload)
    if r:
        print('Bot registered')
    else:
        print(f'It was not possible to register the bot: {r.json()}')
