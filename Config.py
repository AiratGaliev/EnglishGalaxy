import configparser
import os
import platform
import re
from enum import Enum


class Config(Enum):
    @staticmethod
    def get_config():
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config

    @staticmethod
    def get_path_by_platform():
        if platform.system() == 'Windows':
            return 'directories-windows'
        elif platform.system() == 'Linux':
            return 'directories-linux'

    LEVELS = get_config()['main']['levels']
    LEVELS_LIST: list[str] = re.split(r'\s*,\s*', str(LEVELS))
    LEVEL_ID: str = get_config()['main']['level_id']
    AMERICAN_ACCENT: bool = get_config()['main']['american_accent'] == "True"
    BRITISH_ACCENT: bool = get_config()['main']['british_accent'] == "True"
    COLLECTION_MEDIA = os.path.expanduser('~') + get_config()[get_path_by_platform()]['collection_media']
    DOCUMENTS = os.path.expanduser('~') + get_config()['main']['documents']
    CSV_FILES = str(DOCUMENTS) + "/CSV/"
    GENERATED_FILES = str(DOCUMENTS) + "/Generated/"
    EMAIL: str = get_config()['login']['email']
    PASSWORD: str = get_config()['login']['password']
