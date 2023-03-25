import csv
import glob
import os

import requests
from phonemizer import phonemize

from AmericanVoice import AmericanVoice
from BritishVoice import BritishVoice
from Config import Config
from Phrase import Phrase
from Voice import Voice
from VoiceSpeed import VoiceSpeed


def check_file_in_path(phrase_audio: str) -> bool:
    os.chdir(Config.COLLECTION_MEDIA.value)
    files = glob.glob(phrase_audio)
    if len(files) > 0:
        for file in files:
            get_size = os.path.getsize(file)
            return get_size > 10000
    return False


def parse_csv(file_path) -> list[Phrase]:
    phrases: list[Phrase] = []
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            phrase = Phrase(row[0], row[1])
            phrases.append(phrase)
    return phrases


PHRASE_FILE_NAME_TEMPLATE = "eg_{level_id}_l_{lesson_id}_phrase_{phrase_id}_{initials}.wav"
VOICE_STRING = "<li>[sound:{phrase_file_name}]&nbsp;{name}</li>"


def generate_cards(root_deck_name: str, child_deck_name: str, level_id: str, lesson_id: int, regenerate_id: int,
                   regenerate_all_lesson: bool):
    phrases = parse_csv(Config.CSV_FILES.value + root_deck_name + " - " + child_deck_name + '.csv')
    phrase_id = 0
    all_string = "#separator:tab\n" \
                 "#html:true\n" \
                 "#notetype column:1\n" \
                 "#deck column:2\n" \
                 "#tags column:5\n"
    start_string_child_deck_name = child_deck_name
    if lesson_id < 10:
        start_string_child_deck_name = child_deck_name.replace(" ", " 0")
    start_string = "Basic\t{root_deck_name}::{child_deck_name}\t".format(root_deck_name=root_deck_name,
                                                                         child_deck_name=start_string_child_deck_name)
    for phrase in phrases:
        phrase_id = phrase_id + 1
        print("Progress: {:2.1%}".format(phrase_id / len(phrases)))
        all_string += start_string
        translation_original_string = "{translation}\t{original}".format(translation=phrase.translation,
                                                                         original=phrase.original)
        american_string = "<br><br>american listen:<br>{american_transcription}<br><ul>".format(
            american_transcription=phonemize(phrase.original, language='en-us', backend='espeak')).replace('ɹ',
                                                                                                           'r').replace(
            'ɐ', 'a')

        all_string += translation_original_string + american_string

        all_string += crate_example(level_id, lesson_id, phrase_id, regenerate_all_lesson, regenerate_id, phrase,
                                    AmericanVoice.TOM_JOSEPH.value)

        all_string += crate_example(level_id, lesson_id, phrase_id, regenerate_all_lesson, regenerate_id, phrase,
                                    AmericanVoice.SABRINA_INKWELL.value)

        british_string = "</ul><br><br>british listen:<br>{british_transcription}<br><ul>".format(
            british_transcription=phonemize(phrase.original, language='en-gb', backend='espeak')).replace('ɹ',
                                                                                                          'r').replace(
            'ɐ', 'a')
        all_string += british_string

        all_string += crate_example(level_id, lesson_id, phrase_id, regenerate_all_lesson, regenerate_id, phrase,
                                    BritishVoice.RYAN_MAGUIRE.value)

        all_string += crate_example(level_id, lesson_id, phrase_id, regenerate_all_lesson, regenerate_id, phrase,
                                    BritishVoice.MIA_MOUNT.value)

        all_string += "</ul>\n"
    with open(Config.TXT_FILES.value + root_deck_name + " - " + child_deck_name + ".txt", "w") as file:
        file.write(all_string)
        file.close()


def crate_example(level_id: str, lesson_id: int, phrase_id: int, regenerate_all_lesson: bool, regenerate_id: int,
                  phrase: Phrase, voice: Voice) -> str:
    phrase_file_name = PHRASE_FILE_NAME_TEMPLATE.format(level_id=level_id, lesson_id=lesson_id, phrase_id=phrase_id,
                                                        initials=voice.initials)
    is_convert_tts = (not check_file_in_path(phrase_file_name)) or phrase_id == regenerate_id or regenerate_all_lesson
    if is_convert_tts:
        convert_text_to_audio(voice, phrase_file_name, phrase.original, VoiceSpeed.NORMAL.value)
    return VOICE_STRING.format(phrase_file_name=phrase_file_name, name=voice.name)


def convert_text_to_audio(voice: Voice, phrase_file_name: str, text: str, voice_speed: int):
    while True:
        cookies = {
            '__stripe_mid': Config.STRIPE_MID.value,
            '__stripe_sid': Config.STRIPE_SID.value,
            'ACCESS_TOKEN': Config.ACCESS_TOKEN.value,
        }

        headers = {
            'authority': 'studio.lovo.ai',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
            'content-type': 'application/json;charset=UTF-8',
            'dnt': '1',
            'origin': 'https://studio.lovo.ai',
            'referer': 'https://studio.lovo.ai/',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        json_data = {
            "speaker_id": voice.id,
            "text": text,
            "speed": "[{voice_speed},\"false\"]".format(voice_speed=voice_speed),
            "pause": "0",
            "emphasis": "[]",
            "is_custom": False
        }

        with requests.post('https://studio.lovo.ai/api/workspace/convert_audio', cookies=cookies, json=json_data,
                           headers=headers) as response:
            with open(
                    "{collection_media}{phrase_file_name}".format(collection_media=Config.COLLECTION_MEDIA.value,
                                                                  phrase_file_name=phrase_file_name),
                    "wb") as file:
                file.write(response.content)
                file.close()
        if check_file_in_path(phrase_file_name):
            break
