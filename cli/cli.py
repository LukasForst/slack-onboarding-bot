import argparse
import json
from dataclasses import dataclass, fields, field
from typing import Tuple

from dacite import from_dict

from roman import obtain_auth
from charon import register_bot
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
    env_path: str
    roman_url: str = field(default="http://proxy.services.zinfra.io")
    charon_url: str = field(default="http://localhost:8080")
    bot_url: str = field(default="http://bot:8080/slack/events")


def load_config(path: str) -> Config:
    with open(path, 'r') as file:
        data = json.load(file)
        return from_dict(data_class=Config, data=data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare environment for the docker-compose')

    parser.add_argument("--email", "-e", help="Email for the Roman account.")
    parser.add_argument("--password", "-p", help="Password for the Roman account.")

    parser.add_argument("--name", "-n", help="Name of the service, if the account does not exist yet.")
    parser.add_argument("--service-url", "-su", help="URL where is the service running.")

    parser.add_argument("--env-path", "-e", help="File to which should be the secrets printed.")

    parser.add_argument("--roman-url", "-u", default="http://proxy.services.zinfra.io", help="Roman URL")
    parser.add_argument("--charon-url", "-u", default="http://localhost:8080", help="Charon URL")
    parser.add_argument("--bot-url", "-u", default="http://bot:8080/slack/events", help="Bot URL")

    args = parser.parse_args()

    auth = obtain_auth(args.roman_url, args.email, args.password, args.name, args.service_url, "Testing bot.")

    if not auth:
        print('It was not possible to get auth token.')
        exit(1)

    bot_api_key, signing_secret = create_env(args.env_path)
    r = register_bot(args.charon_url, bot_token=simple_bot_token(), signing_secret=signing_secret,
                     bot_api_key=bot_api_key,
                     bot_url=args.bot_url, auth_code=auth)
    if r:
        print('Bot successfully registered.')
    else:
        print('It was not possible to register bot.')
        exit(2)
