#!/usr/bin/env python3

import uuid
import string
import random


def generate_signing_secret() -> str:
    return uuid.uuid4().hex


def generate_bot_token() -> str:
    def generate(alphabet, size):
        return ''.join(random.choice(alphabet) for _ in range(size))

    digits = string.digits
    alphanumeric = digits + string.ascii_letters

    final = ['xoxb', generate(digits, 12), generate(digits, 12), generate(alphanumeric, 24)]
    return '-'.join(final)


def get_env_string() -> str:
    return f'SLACK_SIGNING_SECRET={generate_signing_secret()}\nSLACK_BOT_TOKEN={generate_bot_token()}'


if __name__ == '__main__':
    print(get_env_string())
