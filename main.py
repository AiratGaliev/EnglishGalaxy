from Config import Config
from utils import generate_cards, parse_numeric_array, get_access_token

if __name__ == '__main__':
    levels: list[str] = Config.LEVELS_LIST.value
    level_id = Config.LEVEL_ID.value
    american_accent: bool = Config.AMERICAN_ACCENT.value
    british_accent: bool = Config.BRITISH_ACCENT.value
    collection_media = Config.COLLECTION_MEDIA.value
    documents = Config.DOCUMENTS.value
    email = Config.EMAIL.value
    password = Config.PASSWORD.value
    lessons_id: list[int] = parse_numeric_array("1..50")
    regenerate_exercise_id: int = 0
    generate_all_level: bool = True if input('Generate all levels? y/n (default n):') == 'y' else False
    generate_all_lessons_text: bool = True if input('Generate all lessons text? y/n (default n):') == 'y' else False
    regenerate_all_lessons: bool = True if input('Regenerate all lesson? y/n (default n):') == 'y' else False
    access_token = get_access_token(email, password)
    checked_levels: list[str] = []
    if generate_all_level:
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
            if not (generate_all_lessons_text or regenerate_all_lessons):
                lessons_str = input("Enter generate lessons in the format '1' or '1..50'(default):")
                if lessons_str != '':
                    lessons_id = parse_numeric_array(lessons_str)
                    regenerate_exercise_id = int(input('Regenerate exercise id:'))
        except ValueError:
            input('Not a number')
        for lesson_id in lessons_id:
            generate_cards(level, lesson_id, regenerate_exercise_id, regenerate_all_lessons, american_accent,
                           british_accent, collection_media, documents, access_token)
