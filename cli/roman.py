#!/usr/bin/env python3

import argparse
import os
from typing import Optional

import requests

s = requests.Session()


def silent_print(payload):
    if not os.getenv('SILENT') == 'True':
        print(payload)


def register(url: str, email: str, password: str, service_name: str) -> bool:
    payload = {
        'name': service_name,
        'email': email,
        'password': password
    }
    r = s.post(f"{url}/register", json=payload)
    if r:
        silent_print('Account registered.')
    else:
        silent_print(f'It was not possible to register account: {r.json()}')
    return bool(r)


def login(url: str, email: str, password: str) -> bool:
    payload = {
        'email': email,
        'password': password
    }
    r = s.post(f"{url}/login", json=payload)
    if r:
        silent_print('Login successful.')
    else:
        silent_print(f'It was not possible to login: {r.json()}')
    return bool(r)


def create_service(url: str, name: str, service_url: str, service_summary: str) -> Optional[str]:
    payload = {
        'name': name,
        'url': service_url,
        'summary': service_summary if service_summary else 'Summary not provided by user.'
    }
    r = s.post(f"{url}/service", json=payload)
    if r:
        silent_print('Service created.')
        return r.json()['service_authentication']
    else:
        silent_print(f'It was not possible to create service: {r.json()}')
        return None


def update_service_url(url: str, service_url: str):
    r = s.put(f'{url}/service', json={'url': service_url})
    if r:
        silent_print(f'URL successfully updated to {service_url}')
    else:
        silent_print('It was not possible to update URL.')


def get_auth_code(url: str, service_url: Optional[str]) -> Optional[str]:
    r = s.get(f'{url}/service')
    if r:
        json = r.json()
        auth_code = json.get('service_authentication')
        if auth_code:
            silent_print('Service exists.')

            if service_url and json['webhook'] != service_url:
                silent_print(
                    f'Current service URL: {json["webhook"]} does not match provided: {service_url}. Updating.')
                update_service_url(url, service_url)

            return auth_code
        else:
            silent_print('Service does not exist.')
            return None
    else:
        silent_print(f'Error while getting service info: {r.json()}')
        return None


def obtain_auth(url: str, email: str, password: str,
                service_name: Optional[str] = None,
                service_url: Optional[str] = None,
                service_summary: Optional[str] = None) -> Optional[str]:
    if login(url, email, password):
        silent_print('Login successful')
    elif register(url, email, password, service_name):
        silent_print('Registration was successful, please check your email and run the script again.')
        return None

    auth_code = get_auth_code(url, service_url)

    if not auth_code:
        auth_code = create_service(url, service_name, service_url, service_summary)

    if not auth_code:
        silent_print('It was not possible to create service.')
        raise Exception('Not possible to obtain auth.')

    return auth_code


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login or create account in Roman')

    parser.add_argument("--email", "-e", help="Email for the account.")
    parser.add_argument("--password", "-p", help="Password for the account.")

    parser.add_argument("--url", "-u", default="http://proxy.services.zinfra.io", help="Roman URL")
    parser.add_argument("--name", "-n", help="Name of the service, if the account does not exist yet.")
    parser.add_argument("--service-url", "-su", help="URL where is the service running.")
    parser.add_argument("--summary", "-sm", help="Summary of the service.")

    parser.add_argument("--silent", "-s", action='store_const', const='True', help="Run in silent mode.",
                        default='False')

    args = parser.parse_args()

    os.environ['SILENT'] = str(args.silent)

    auth = obtain_auth(args.url, args.email, args.password, args.name, args.service_url, args.summary)

    if auth:
        if args.silent == 'True':
            print(auth)
        else:
            silent_print(f'Auth code: {auth}')
