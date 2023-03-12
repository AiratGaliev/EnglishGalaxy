import configparser
from enum import Enum


class Config(Enum):
    @staticmethod
    def _get_config():
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config

    LEVEL_ID = _get_config()['main']['level_id']
    COLLECTION_MEDIA = _get_config()['directories']['collection_media']
    CSV_FILES = _get_config()['directories']['csv_files']
    TXT_FILES = _get_config()['directories']['txt_files']
    STRIPE_MID = _get_config()['cookies']['stripe_mid']
    STRIPE_SID = _get_config()['cookies']['stripe_sid']
    ACCESS_TOKEN = _get_config()['cookies']['access_token']
