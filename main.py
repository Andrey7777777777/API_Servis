import os
import sys
import requests
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


def entered_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('link', help="Link you want to shorten")
    args = parser.parse_args()
    return args.link

def shorten_link(headers, url):
    payload = {"long_url": url, }
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', json=payload, headers=headers)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(headers, url):
    parsed_url = urlparse(url)
    link = f'{parsed_url.netloc}{parsed_url.path}'
    link_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    clicks_response = requests.get(link_url, headers=headers)
    clicks_response.raise_for_status()
    clicks = clicks_response.json()['total_clicks']
    return clicks


def is_bitlink(headers, url):
    parsed_url = urlparse(url)
    url = f"{parsed_url.netloc}{parsed_url.path}"
    for_bitlink_url = f"https://api-ssl.bitly.com/v4/bitlinks/{url}"
    response = requests.get(for_bitlink_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    url = entered_arguments()
    secret_token = os.environ['BITLY_TOKEN']
    headers = {"Authorization": f"Bearer {secret_token}"}
    if is_bitlink(headers, url):
        try:
            clicks = count_clicks(headers, url)
        except requests.exceptions.HTTPError:
            print("Вы ввели неправильную ссылку или неверный токен.")
            sys.exit(0)
        print(f'Количество кликов по ссылке {clicks}')
    else:
        try:
            bitlink = shorten_link(headers, url)
        except requests.exceptions.HTTPError:
            print("Вы ввели неправильную ссылку или неверный токен.")
            sys.exit(0)
        print(f'Битлинк {bitlink}')


if __name__ == '__main__':
    main()