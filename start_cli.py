import os

from config.Config import Config
from logic.utils import generate_cards, parse_numeric_array, get_access_token, get_file_paths, clean_up_duplicates

if __name__ == '__main__':
    levels: list[str] = Config.LEVELS_LIST.value
    folders = [level.upper() for level in levels]
    documents = Config.DOCUMENTS.value
    folder_paths: list[str] = [os.path.join(documents + "CSV", folder) for folder in folders]
    file_paths: list[str] = get_file_paths(folder_paths)
    clean_up_duplicates(file_paths)
    level_id = Config.LEVEL_ID.value
    american_accent: bool = Config.AMERICAN_ACCENT.value
    british_accent: bool = Config.BRITISH_ACCENT.value
    collection_media = Config.COLLECTION_MEDIA.value
    email = Config.EMAIL.value
    password = Config.PASSWORD.value
    lessons_id: list[int] = parse_numeric_array("1..50")
    regenerate_exercise_id: int = 0
    generate_all_levels: bool = True if input('Generate all levels? y/n (default n):') == 'y' else False
    generate_texts_of_all_levels: bool = False
    generate_lessons: bool = False
    if not generate_all_levels:
        generate_texts_of_all_levels = True if input('Generate texts of all levels? y/n (default n):') == 'y' else False
    else:
        generate_lessons = True
    if not (generate_all_levels or generate_texts_of_all_levels):
        generate_lessons = True if input('Generate lessons? y/n (default n):') == 'y' else False
    access_token = get_access_token(email, password)
    checked_levels: list[str] = []
    if generate_all_levels or generate_texts_of_all_levels:
        checked_levels.extend(levels)
    else:
        checked_levels.append(levels[int(level_id)]) if level_id != '' else checked_levels.extend(levels)
    for level in checked_levels:
        try:
            print("Lessons level is {level}".format(level=level.upper()))
            if american_accent:
                print("An American accent has been chosen")
            if british_accent:
                print("A British accent has been chosen")
            if not (generate_all_levels or generate_texts_of_all_levels):
                lessons_str = input("Enter generate lessons in the format '1' or '1..50'(default):")
                if lessons_str != '':
                    lessons_id = parse_numeric_array(lessons_str)
                    regenerate_exercise_id = int(input('Regenerate exercise id:'))
        except ValueError:
            print('Not a number')
        for lesson_id in lessons_id:
            generate_cards(level, lesson_id, regenerate_exercise_id, generate_lessons, american_accent,
                           british_accent, collection_media, documents, access_token)
