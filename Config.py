import configparser
import os
import platform
from enum import Enum


class Config(Enum):
    @staticmethod
    def _get_config():
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config

    @staticmethod
    def _get_path_by_platform():
        if platform.system() == 'Windows':
            return 'directories-windows'
        elif platform.system() == 'Linux':
            return 'directories-linux'

    LEVEL_ID = _get_config()['main']['level_id']
    COLLECTION_MEDIA = os.path.expanduser('~') + _get_config()[_get_path_by_platform()]['collection_media']
    CSV_FILES = os.path.expanduser('~') + _get_config()[_get_path_by_platform()]['csv_files']
    TXT_FILES = os.path.expanduser('~') + _get_config()[_get_path_by_platform()]['txt_files']
    STRIPE_MID = _get_config()['cookies']['stripe_mid']
    STRIPE_SID = _get_config()['cookies']['stripe_sid']
    ACCESS_TOKEN = _get_config()['cookies']['access_token']
