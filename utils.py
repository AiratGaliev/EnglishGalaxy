import csv
import glob
import os
import requests
from phonemizer import phonemize
from AmericanVoice import AmericanVoice
from BritishVoice import BritishVoice
from Phrase import Phrase
from Voice import Voice
from VoiceSpeed import VoiceSpeed

COLLECTION_MEDIA = '/home/airat/.local/share/Anki2/User 1/collection.media/'


def check_file_in_path(phrase_audio: str) -> bool:
    os.chdir(COLLECTION_MEDIA)
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


def generate_cards(root_deck_name: str, child_deck_name: str, level_id: str, lesson_id: int, regenerate_id: int,
                   regenerate_all: bool):
    phrases = parse_csv("/home/airat/Documents/English Galaxy/CSV/" + root_deck_name + " - " + child_deck_name + '.csv')
    phrase_id = 0
    all_string = "#separator:tab\n" \
                 "#html:true\n" \
                 "#notetype column:1\n" \
                 "#deck column:2\n" \
                 "#tags column:5\n"
    start_string = "Basic\t{root_deck_name}::{child_deck_name}\t".format(root_deck_name=root_deck_name,
                                                                         child_deck_name=child_deck_name)
    voice_string = "<li>[sound:{phrase_audio}]&nbsp;{name}</li>"
    phrase_audio_original = "eg_{level_id}_l_{lesson_id}_phrase_{phrase_id}_{initials}.wav"
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

        phrase_audio = phrase_audio_original.format(level_id=level_id, lesson_id=lesson_id, phrase_id=phrase_id,
                                                    initials=AmericanVoice.AUSTIN_HOPKINS.value.initials)
        is_convert_text_to_audio = (not check_file_in_path(
            phrase_audio)) or phrase_id == regenerate_id or regenerate_all
        if is_convert_text_to_audio:
            convert_text_to_audio(AmericanVoice.AUSTIN_HOPKINS.value, phrase_audio,
                                  phrase.original,
                                  VoiceSpeed.NORMAL.value)
        all_string += voice_string.format(phrase_audio=phrase_audio, name=AmericanVoice.AUSTIN_HOPKINS.value.name)

        phrase_audio = phrase_audio_original.format(level_id=level_id, lesson_id=lesson_id, phrase_id=phrase_id,
                                                    initials=AmericanVoice.SHARON_HUANG.value.initials)
        is_convert_text_to_audio = (not check_file_in_path(
            phrase_audio)) or phrase_id == regenerate_id or regenerate_all
        if is_convert_text_to_audio:
            convert_text_to_audio(AmericanVoice.SHARON_HUANG.value, phrase_audio, phrase.original,
                                  VoiceSpeed.NORMAL.value)
        all_string += voice_string.format(phrase_audio=phrase_audio, name=AmericanVoice.SHARON_HUANG.value.name)

        phrase_audio = phrase_audio_original.format(level_id=level_id, lesson_id=lesson_id, phrase_id=phrase_id,
                                                    initials=AmericanVoice.TIM_CALKNEY.value.initials)
        is_convert_text_to_audio = (not check_file_in_path(
            phrase_audio)) or phrase_id == regenerate_id or regenerate_all
        if is_convert_text_to_audio:
            convert_text_to_audio(AmericanVoice.TIM_CALKNEY.value, phrase_audio, phrase.original,
                                  VoiceSpeed.NORMAL.value)
        all_string += voice_string.format(phrase_audio=phrase_audio, name=AmericanVoice.TIM_CALKNEY.value.name)

        phrase_audio = phrase_audio_original.format(level_id=level_id, lesson_id=lesson_id, phrase_id=phrase_id,
                                                    initials=AmericanVoice.SUSAN_COLE.value.initials)
        is_convert_text_to_audio = (not check_file_in_path(
            phrase_audio)) or phrase_id == regenerate_id or regenerate_all
        if is_convert_text_to_audio:
            convert_text_to_audio(AmericanVoice.SUSAN_COLE.value, phrase_audio, phrase.original,
                                  VoiceSpeed.NORMAL.value)
        all_string += voice_string.format(phrase_audio=phrase_audio, name=AmericanVoice.SUSAN_COLE.value.name)

        british_string = "</ul><br><br>british listen:<br>{british_transcription}<br><ul>".format(
            british_transcription=phonemize(phrase.original, language='en-gb', backend='espeak')).replace('ɹ',
                                                                                                          'r').replace(
            'ɐ', 'a')
        all_string += british_string

        phrase_audio = phrase_audio_original.format(level_id=level_id, lesson_id=lesson_id, phrase_id=phrase_id,
                                                    initials=BritishVoice.RYAN_MAGUIRE.value.initials)
        is_convert_text_to_audio = (not check_file_in_path(
            phrase_audio)) or phrase_id == regenerate_id or regenerate_all
        if is_convert_text_to_audio:
            convert_text_to_audio(BritishVoice.RYAN_MAGUIRE.value, phrase_audio, phrase.original,
                                  VoiceSpeed.NORMAL.value)
        all_string += voice_string.format(phrase_audio=phrase_audio, name=BritishVoice.RYAN_MAGUIRE.value.name)

        phrase_audio = phrase_audio_original.format(level_id=level_id, lesson_id=lesson_id, phrase_id=phrase_id,
                                                    initials=BritishVoice.MIA_MOUNT.value.initials)
        is_convert_text_to_audio = (not check_file_in_path(
            phrase_audio)) or phrase_id == regenerate_id or regenerate_all
        if is_convert_text_to_audio:
            convert_text_to_audio(BritishVoice.MIA_MOUNT.value, phrase_audio, phrase.original, VoiceSpeed.NORMAL.value)
        all_string += voice_string.format(phrase_audio=phrase_audio, name=BritishVoice.MIA_MOUNT.value.name) + "</ul>\n"
    with open("/home/airat/Documents/English Galaxy/Generated/" + root_deck_name + " - " + child_deck_name + ".txt",
              "w") as file:
        file.write(all_string)
        file.close()


def convert_text_to_audio(voice: Voice, phrase_audio, text, voice_speed):
    while True:
        cookies = {
            '__stripe_mid': 'c8ce967b-bc46-4bfe-9868-1e2966413147a67190',
            '__stripe_sid': '02b54afe-d62e-483b-8c0c-89fe97afa6c3208c0f',
            'ACCESS_TOKEN': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImhlY2F0YTUzNDRAd2lmYW1lLmNvbSIsInN1YiI6IjYzZjdjMzJmMzA5YWEzYWE5NGNmMDg2OSIsImlhdCI6MTY3NzE4MTc2NiwiZXhwIjoxNjc3Nzg2NTY2fQ.prxfqSkFgRqxSVqcnywWW52V4xkC7kGxKTJiEj6qa7k',
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
                    "{collection_media}{phrase_audio}".format(collection_media=COLLECTION_MEDIA,
                                                              phrase_audio=phrase_audio),
                    "wb") as file:
                file.write(response.content)
                file.close()
        if check_file_in_path(phrase_audio):
            break
