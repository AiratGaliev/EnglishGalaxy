import configparser
import os
import platform
from enum import Enum

import requests


def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def get_path_by_platform():
    if platform.system() == 'Windows':
        return 'directories-windows'
    elif platform.system() == 'Linux':
        return 'directories-linux'


def get_access_token() -> str:
    email: str = get_config()['login']['email']
    password: str = get_config()['login']['password']
    json_data = {
        "email": email,
        "password": password
    }
    with requests.post('https://gateway.lovo.ai/auth/login/email', json=json_data) as response:
        response_json = response.json()
        access_token = response_json['data']['accessToken']
        return access_token


class Config(Enum):
    LEVEL_ID = get_config()['main']['level_id']
    AMERICAN_ACCENT: bool = get_config()['main']['american_accent'] == "True"
    BRITISH_ACCENT: bool = get_config()['main']['british_accent'] == "True"
    COLLECTION_MEDIA = os.path.expanduser('~') + get_config()[get_path_by_platform()]['collection_media']
    CSV_FILES = os.path.expanduser('~') + get_config()[get_path_by_platform()]['csv_files']
    TXT_FILES = os.path.expanduser('~') + get_config()[get_path_by_platform()]['txt_files']
    ACCESS_TOKEN = get_access_token()
