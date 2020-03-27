import requests
import re
from pprint import pprint
import time

def fetch(url):
    response = requests.get(url)
    if response.status_code == 200 or response.status_code == 201:
        if response.text is not "":
            return response.json()
        else:
            time.sleep(3.5)
            return fetch(url)
    else:
        return None

def build_url(**kwargs):
    regexp = re.compile(r"\{(.*?)\}")
    url = kwargs.get('url')
    params = kwargs.get('params')
    for match in regexp.findall(url):
        url = url.replace("{"+match+"}", params[match])
    return url

def handle_call(**kwargs):
    url = kwargs.get('url')
    if 'params' in kwargs and '{' in url and '}' in url:
        url = build_url(**kwargs)
    return fetch(url)