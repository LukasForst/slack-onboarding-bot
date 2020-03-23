#!/usr/bin/env python3

import argparse
import json

from dataclasses import dataclass, field
from typing import Tuple
from dacite import from_dict

from charon import register_bot
from roman import obtain_auth
from secrets import generate_signing_secret, generate_bot_token


def simple_bot_token() -> str:
    return "some-bot-token"


def get_env_string(token, signing) -> str:
    return f'SLACK_SIGNING_SECRET={signing}\nSLACK_BOT_TOKEN={token}'


def create_env(env_path: str) -> Tuple[str, str]:
    token, secret = generate_bot_token(), generate_signing_secret()
    with open(env_path, 'w') as f:
        f.write(get_env_string(token, secret))
    return token, secret


@dataclass(frozen=True)
class Config:
    email: str
    password: str
    service_name: str
    service_url: str
    bot_summary: str = field(default='Testing Bot for Charon.')
    roman_url: str = field(default="http://proxy.services.zinfra.io")
    charon_url: str = field(default="http://localhost:8080")
    bot_url: str = field(default="http://bot:8080/slack/events")


def load_config(path: str) -> Config:
    with open(path, 'r') as file:
        data = json.load(file)
        return from_dict(data_class=Config, data=data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare environment for the docker-compose')

    parser.add_argument("--config", "-c", help="Path to configuration file.")
    parser.add_argument("--env", "-e", help="Path to .env file for secrets writing")
    args = parser.parse_args()

    config = load_config(args.config)

    auth = obtain_auth(config.roman_url, config.email, config.password, config.service_name, config.service_url,
                       config.bot_summary)

    if not auth:
        print('It was not possible to get auth token.')
        exit(1)

    bot_api_key, signing_secret = create_env(args.env)
    r = register_bot(config.charon_url,
                     bot_token=simple_bot_token(),
                     signing_secret=signing_secret,
                     bot_api_key=bot_api_key,
                     bot_url=config.bot_url,
                     auth_code=auth)
    if r:
        print('Bot successfully registered.')
    else:
        print('It was not possible to register bot.')
        exit(2)
