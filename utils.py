import csv
import glob
import multiprocessing
import os

import requests
from phonemizer.backend import EspeakBackend

from Accent import Accent
from AmericanVoice import AmericanVoice
from BritishVoice import BritishVoice
from Config import Config
from Phrase import Phrase
from Voice import Voice
from VoiceSpeed import VoiceSpeed

phonemizer_en_us = EspeakBackend(language='en-us')
phonemizer_en_gb = EspeakBackend(language='en-gb')


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
    with open(file_path, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            phrase = Phrase(row[0], row[1])
            phrases.append(phrase)
            del phrase
    return phrases


PHRASE_FILE_NAME_TEMPLATE = "eg_{level_id}_l_{lesson_id}_phrase_{phrase_id}_{initials}.wav"
VOICE_STRING = "<li>[sound:{phrase_file_name}]&nbsp;{name}</li>"


def parse_numeric_array(input_string):
    try:
        if '..' in input_string:
            start, end = map(int, input_string.split('..'))
            return list(range(start, end + 1))
        else:
            return [int(input_string)]
    except ValueError:
        raise ValueError("Incorrect input string format. Use the format '1' or '1..10'.")


def generate_cards(level_id: str, lesson_id: int, regenerate_id: int, regenerate_all_lesson: bool, accent: str):
    root_deck_name: str = 'English Galaxy {level_id}'.format(level_id=level_id.upper())
    child_deck_name: str = 'Lesson {lesson_id}'.format(lesson_id=lesson_id)
    phrases = parse_csv(
        Config.CSV_FILES.value + level_id.upper() + "/" + root_deck_name + " - " + child_deck_name + '.csv')

    if regenerate_all_lesson:
        print("Regenerating all lesson is progress")
        generate_all_text_to_audio(level_id, lesson_id, phrases)

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
        all_string += start_string
        translation_original_string = "{translation}\t{original}".format(translation=phrase.translation,
                                                                         original=phrase.original)
        if accent == Accent.AMERICAN.value:
            american_transcription = phonemizer_en_us.phonemize([phrase.original])[0]
            american_transcription = american_transcription.replace('ɹ', 'r')
            american_transcription = american_transcription.replace('ɐ', 'a')
            american_string = "<br>{american_transcription}<br><ul>".format(
                american_transcription=american_transcription)

            all_string += translation_original_string + american_string

            phrase_file_name = PHRASE_FILE_NAME_TEMPLATE.format(level_id=level_id, lesson_id=lesson_id,
                                                                phrase_id=phrase_id,
                                                                initials=AmericanVoice.MALE.value.initials)
            is_convert_tts = (not check_file_in_path(phrase_file_name)) or phrase_id == regenerate_id
            if is_convert_tts:
                convert_text_to_audio(AmericanVoice.MALE.value, phrase_file_name, phrase.original)
            all_string += VOICE_STRING.format(phrase_file_name=phrase_file_name,
                                              name=AmericanVoice.MALE.value.name)

            phrase_file_name = PHRASE_FILE_NAME_TEMPLATE.format(level_id=level_id, lesson_id=lesson_id,
                                                                phrase_id=phrase_id,
                                                                initials=AmericanVoice.FEMALE.value.initials)
            is_convert_tts = (not check_file_in_path(phrase_file_name)) or phrase_id == regenerate_id
            if is_convert_tts:
                convert_text_to_audio(AmericanVoice.FEMALE.value, phrase_file_name, phrase.original)
            all_string += VOICE_STRING.format(phrase_file_name=phrase_file_name,
                                              name=AmericanVoice.FEMALE.value.name)

        if accent == Accent.BRITISH.value:
            british_transcription = phonemizer_en_gb.phonemize([phrase.original])[0]
            british_transcription = british_transcription.replace('ɹ', 'r')
            british_transcription = british_transcription.replace('ɐ', 'a')
            british_string = "<br>{british_transcription}<br><ul>".format(
                british_transcription=british_transcription)
            all_string += british_string

            phrase_file_name = PHRASE_FILE_NAME_TEMPLATE.format(level_id=level_id, lesson_id=lesson_id,
                                                                phrase_id=phrase_id,
                                                                initials=BritishVoice.MALE.value.initials)
            is_convert_tts = (not check_file_in_path(phrase_file_name)) or phrase_id == regenerate_id
            if is_convert_tts:
                convert_text_to_audio(BritishVoice.MALE.value, phrase_file_name, phrase.original)
            all_string += VOICE_STRING.format(phrase_file_name=phrase_file_name,
                                              name=BritishVoice.MALE.value.name)

            phrase_file_name = PHRASE_FILE_NAME_TEMPLATE.format(level_id=level_id, lesson_id=lesson_id,
                                                                phrase_id=phrase_id,
                                                                initials=BritishVoice.FEMALE.value.initials)
            is_convert_tts = (not check_file_in_path(phrase_file_name)) or phrase_id == regenerate_id
            if is_convert_tts:
                convert_text_to_audio(BritishVoice.FEMALE.value, phrase_file_name, phrase.original)
            all_string += VOICE_STRING.format(phrase_file_name=phrase_file_name, name=BritishVoice.FEMALE.value.name)

        all_string += "</ul>\n"
    with open(Config.TXT_FILES.value + level_id.upper() + "/" + root_deck_name + " - " + child_deck_name + ".txt", "w",
              encoding='utf-8') as file:
        file.write(all_string)
        file.close()

    del phrase_file_name
    del phrases

    print('Level {level_id} lesson {lesson_id} done!'.format(level_id=level_id.upper(), lesson_id=lesson_id))


def map_convert_text_to_audio(args):
    phrase_id, level_id, lesson_id, phrases = args
    phrase = phrases[phrase_id]
    phrase_id = phrase_id + 1
    phrase_file_name_a_v_m = PHRASE_FILE_NAME_TEMPLATE.format(level_id=level_id, lesson_id=lesson_id,
                                                              phrase_id=phrase_id,
                                                              initials=AmericanVoice.MALE.value.initials)
    phrase_file_name_a_v_f = PHRASE_FILE_NAME_TEMPLATE.format(level_id=level_id, lesson_id=lesson_id,
                                                              phrase_id=phrase_id,
                                                              initials=AmericanVoice.FEMALE.value.initials)
    phrase_file_name_b_v_m = PHRASE_FILE_NAME_TEMPLATE.format(level_id=level_id, lesson_id=lesson_id,
                                                              phrase_id=phrase_id,
                                                              initials=BritishVoice.MALE.value.initials)
    phrase_file_name_b_v_f = PHRASE_FILE_NAME_TEMPLATE.format(level_id=level_id, lesson_id=lesson_id,
                                                              phrase_id=phrase_id,
                                                              initials=BritishVoice.FEMALE.value.initials)
    convert_text_to_audio(AmericanVoice.MALE.value, phrase_file_name_a_v_m, phrase.original)
    convert_text_to_audio(AmericanVoice.FEMALE.value, phrase_file_name_a_v_f, phrase.original)
    convert_text_to_audio(BritishVoice.MALE.value, phrase_file_name_b_v_m, phrase.original)
    convert_text_to_audio(BritishVoice.FEMALE.value, phrase_file_name_b_v_f, phrase.original)


def generate_all_text_to_audio(level_id, lesson_id, phrases: list[Phrase]):
    num_tasks = len(phrases)
    with multiprocessing.Pool() as pool:
        tasks = [(phrase_id, level_id, lesson_id, phrases) for phrase_id in range(num_tasks)]
        chunksize = len(tasks) // multiprocessing.cpu_count()
        pool.map(map_convert_text_to_audio, tasks, chunksize=chunksize)


def convert_text_to_audio(voice: Voice, phrase_file_name: str, text: str, voice_speed: int = VoiceSpeed.NORMAL.value):
    while True:
        cookies = {
            'ACCESS_TOKEN': Config.ACCESS_TOKEN.value
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
