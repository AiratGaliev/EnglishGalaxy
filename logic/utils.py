import glob
import multiprocessing
import os
import re
import time

import pandas as pd
import requests
import streamlit as st
from phonemizer.backend import EspeakBackend

from models.AmericanVoice import AmericanVoice
from models.BritishVoice import BritishVoice
from models.Phrase import Phrase
from models.Voice import Voice
from models.VoiceSpeed import VoiceSpeed

phonemizer_en_us = EspeakBackend(language='en-us')
phonemizer_en_gb = EspeakBackend(language='en-gb')


@st.cache_resource
def get_access_token(email: str, password: str) -> str:
    json_data = {
        "email": email,
        "password": password
    }
    with requests.post('https://gateway.lovo.ai/auth/login/email', json=json_data) as response:
        response_json = response.json()
        access_token = response_json['data']['accessToken']
        return access_token


def check_file_in_path(path: str, file_name: str) -> bool:
    os.chdir(path)
    files = glob.glob(file_name)
    if len(files) > 0:
        for file in files:
            get_size = os.path.getsize(file)
            return get_size > 10000
    return False


def load_keywords(filename):
    df = pd.read_csv(filename, header=None, names=['keyword', 'hint'])
    return dict(zip(df['keyword'], df['hint']))


def process_translation(english_text, russian_translation, keyword_dict):
    hints = []
    for keyword, hint in keyword_dict.items():
        if keyword != '*':
            for match in re.finditer(r'\b{}\b'.format(keyword), english_text, re.IGNORECASE):
                hints.append((match.start(), hint))
    hints.sort()
    for hint in hints:
        if f'{hint[1]}' not in russian_translation:
            russian_translation += f' ({hint[1]})'
    return russian_translation


def remove_hints(text, exceptions):
    if exceptions:
        pattern = r'\s*\((?!{})[^)]*\)\s*'.format('|'.join(re.escape(e) for e in exceptions))
    else:
        pattern = r'\s*\([^)]*\)\s*'
    return re.sub(pattern, '', text)


def clean_up_csv(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'\n+$', '', content)
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write(content)


def parse_csv(file_path) -> list[Phrase]:
    df = pd.read_csv(file_path, header=None, names=['original', 'translation'])
    phrases: list[Phrase] = [Phrase(row['original'], row['translation']) for index, row in df.iterrows()]
    return phrases


PHRASE_FILE_NAME_TEMPLATE = "eg_{level}_l_{lesson_id}_phrase_{phrase_id}_{initials}.wav"
VOICE_STRING = "<li>[sound:{phrase_file_name}]&nbsp;{name}</li>"


def parse_numeric_array(input_string):
    try:
        if '..' in input_string:
            start, end = map(int, input_string.split('..'))
            return list(range(start, end + 1))
        else:
            return [int(input_string)]
    except ValueError:
        raise ValueError("Incorrect input string format. Use the format '1' or '1..50'.")


def generate_cards(level: str, lesson_id: int, regenerate_exercise_id: int, regenerate_lessons: bool,
                   american_accent: bool, british_accent: bool, collection_media: str, documents: str,
                   access_token: str):
    root_deck_name: str = 'English Galaxy {level}'.format(level=level.upper())
    child_deck_name: str = 'Lesson {lesson_id}'.format(lesson_id=lesson_id)
    keyword_dict = load_keywords(documents + 'Keywords.csv')
    exceptions = keyword_dict.get('*', '').split('|') if '*' in keyword_dict else []
    csv_file = documents + "/CSV/" + level.upper() + "/" + root_deck_name + " - " + child_deck_name + '.csv'
    df = pd.read_csv(csv_file, header=None, names=['english_text', 'russian_translation'])
    df['russian_translation'] = df['russian_translation'].apply(lambda text: remove_hints(text, exceptions))
    df['russian_translation'] = df.apply(
        lambda row: process_translation(row['english_text'], row['russian_translation'], keyword_dict), axis=1)
    df.to_csv(csv_file, index=False, header=False)
    clean_up_csv(csv_file)
    phrases: list[Phrase] = parse_csv(csv_file)

    if regenerate_lessons:
        st.info("Regenerating level {level} lesson {lesson_id} is progress".format(level=level.upper(),
                                                                                   lesson_id=lesson_id), icon="ℹ️")
        generate_all_text_to_audio(level, lesson_id, collection_media, phrases, american_accent, british_accent,
                                   access_token)

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
        if american_accent:
            american_transcription = phonemizer_en_us.phonemize([phrase.original])[0]
            american_transcription = american_transcription.replace('ɹ', 'r')
            american_transcription = american_transcription.replace('ɐ', 'a')
            american_string = "<br>{american_transcription}<br><ul>".format(
                american_transcription=american_transcription)

            all_string += translation_original_string + american_string

            phrase_file_name = PHRASE_FILE_NAME_TEMPLATE.format(level=level, lesson_id=lesson_id, phrase_id=phrase_id,
                                                                initials=AmericanVoice.MALE.value.initials)
            is_convert_tts = (not check_file_in_path(collection_media,
                                                     phrase_file_name)) or phrase_id == regenerate_exercise_id
            if is_convert_tts:
                convert_text_to_audio(AmericanVoice.MALE.value, collection_media, phrase_file_name, access_token,
                                      phrase.original)
            all_string += VOICE_STRING.format(phrase_file_name=phrase_file_name,
                                              name=AmericanVoice.MALE.value.name)

            phrase_file_name = PHRASE_FILE_NAME_TEMPLATE.format(level=level, lesson_id=lesson_id, phrase_id=phrase_id,
                                                                initials=AmericanVoice.FEMALE.value.initials)
            is_convert_tts = (not check_file_in_path(collection_media,
                                                     phrase_file_name)) or phrase_id == regenerate_exercise_id
            if is_convert_tts:
                convert_text_to_audio(AmericanVoice.FEMALE.value, collection_media, phrase_file_name, access_token,
                                      phrase.original)
            all_string += VOICE_STRING.format(phrase_file_name=phrase_file_name,
                                              name=AmericanVoice.FEMALE.value.name)

        if british_accent:
            british_transcription = phonemizer_en_gb.phonemize([phrase.original])[0]
            british_transcription = british_transcription.replace('ɹ', 'r')
            british_transcription = british_transcription.replace('ɐ', 'a')
            british_string = "<br>{british_transcription}<br><ul>".format(
                british_transcription=british_transcription)
            all_string += british_string

            phrase_file_name = PHRASE_FILE_NAME_TEMPLATE.format(level=level, lesson_id=lesson_id, phrase_id=phrase_id,
                                                                initials=BritishVoice.MALE.value.initials)
            is_convert_tts = (not check_file_in_path(collection_media,
                                                     phrase_file_name)) or phrase_id == regenerate_exercise_id
            if is_convert_tts:
                convert_text_to_audio(BritishVoice.MALE.value, collection_media, phrase_file_name, access_token,
                                      phrase.original)
            all_string += VOICE_STRING.format(phrase_file_name=phrase_file_name,
                                              name=BritishVoice.MALE.value.name)

            phrase_file_name = PHRASE_FILE_NAME_TEMPLATE.format(level=level, lesson_id=lesson_id, phrase_id=phrase_id,
                                                                initials=BritishVoice.FEMALE.value.initials)
            is_convert_tts = (not check_file_in_path(collection_media,
                                                     phrase_file_name)) or phrase_id == regenerate_exercise_id
            if is_convert_tts:
                convert_text_to_audio(BritishVoice.FEMALE.value, collection_media, phrase_file_name, access_token,
                                      phrase.original)
            all_string += VOICE_STRING.format(phrase_file_name=phrase_file_name, name=BritishVoice.FEMALE.value.name)

        all_string += "</ul>\n"
    with open(documents + "/Generated/" + level.upper() + "/" + root_deck_name + " - " + child_deck_name + ".txt", "w",
              encoding='utf-8') as file:
        file.write(all_string)
        file.close()

    del phrase_file_name
    del phrases

    st.success('Level {level} lesson {lesson_id} done!'.format(level=level.upper(), lesson_id=lesson_id), icon="✅")


def map_convert_text_to_audio(args):
    phrase_id, level, lesson_id, collection_media, phrases, american_accent, british_accent, access_token = args
    phrase = phrases[phrase_id]
    phrase_id = phrase_id + 1
    if american_accent:
        phrase_file_name_a_v_m = PHRASE_FILE_NAME_TEMPLATE.format(level=level, lesson_id=lesson_id, phrase_id=phrase_id,
                                                                  initials=AmericanVoice.MALE.value.initials)
        phrase_file_name_a_v_f = PHRASE_FILE_NAME_TEMPLATE.format(level=level, lesson_id=lesson_id, phrase_id=phrase_id,
                                                                  initials=AmericanVoice.FEMALE.value.initials)
        convert_text_to_audio(AmericanVoice.MALE.value, collection_media, phrase_file_name_a_v_m, access_token,
                              phrase.original)
        convert_text_to_audio(AmericanVoice.FEMALE.value, collection_media, phrase_file_name_a_v_f, access_token,
                              phrase.original)
    if british_accent:
        phrase_file_name_b_v_m = PHRASE_FILE_NAME_TEMPLATE.format(level=level, lesson_id=lesson_id, phrase_id=phrase_id,
                                                                  initials=BritishVoice.MALE.value.initials)
        phrase_file_name_b_v_f = PHRASE_FILE_NAME_TEMPLATE.format(level=level, lesson_id=lesson_id, phrase_id=phrase_id,
                                                                  initials=BritishVoice.FEMALE.value.initials)
        convert_text_to_audio(BritishVoice.MALE.value, collection_media, phrase_file_name_b_v_m, access_token,
                              phrase.original)
        convert_text_to_audio(BritishVoice.FEMALE.value, collection_media, phrase_file_name_b_v_f, access_token,
                              phrase.original)


def generate_all_text_to_audio(level, lesson_id, collection_media, phrases, american_accent, british_accent,
                               access_token):
    num_tasks = len(phrases)
    with multiprocessing.Pool() as pool:
        tasks = [(phrase_id, level, lesson_id, collection_media, phrases, american_accent, british_accent, access_token)
                 for phrase_id in range(num_tasks)]
        chunksize = len(tasks) // multiprocessing.cpu_count()
        pool.map(map_convert_text_to_audio, tasks, chunksize=chunksize)


def convert_text_to_audio(voice: Voice, collection_media: str, phrase_file_name: str, access_token: str, text: str,
                          voice_speed: int = VoiceSpeed.NORMAL.value):
    max_retries = 50
    retries = 0

    cookies = {
        'ACCESS_TOKEN': access_token
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
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }

    json_data = {
        "speaker_id": voice.id,
        "text": text,
        "speed": "[{voice_speed},\"false\"]".format(voice_speed=voice_speed),
        "pause": "0",
        "emphasis": "[]",
        "is_custom": False
    }

    while retries < max_retries:
        try:
            with requests.post('https://studio.lovo.ai/api/workspace/convert_audio', cookies=cookies, json=json_data,
                               headers=headers) as response:
                with open(
                        "{collection_media}{phrase_file_name}".format(collection_media=collection_media,
                                                                      phrase_file_name=phrase_file_name),
                        "wb") as file:
                    file.write(response.content)
                    file.close()
            if check_file_in_path(collection_media, phrase_file_name):
                break
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
            retries += 1
        except Exception as err:
            st.error(f"An error occurred: {err}")
            retries += 1

        if retries < max_retries:
            st.warning(f"Retrying in 5 seconds... (Attempt {retries}/{max_retries})", icon="⚠️")
            time.sleep(5)
