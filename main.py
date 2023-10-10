from Config import Config
from utils import generate_cards, parse_numeric_array

if __name__ == '__main__':
    levels: list[str] = Config.LEVELS.value
    level_id = Config.LEVEL_ID.value
    american_accent: bool = Config.AMERICAN_ACCENT.value
    british_accent: bool = Config.BRITISH_ACCENT.value
    lessons_id: list[int] = []
    regenerate_id: int = 0
    regenerate_all_lesson: bool = False
    regenerate_all_level: bool = False
    checked_levels: list[str] = []
    checked_levels.append(levels[int(level_id)]) if level_id != '' else checked_levels.extend(levels)
    for level in checked_levels:
        try:
            print("Lessons level is {level}".format(level=level.upper()))
            if american_accent:
                print("An American accent has been chosen")
            if british_accent:
                print("A British accent has been chosen")
            lessons = input("Enter lessons in the format '1' or '1..50'(default):")
            lessons_id = parse_numeric_array("1..50" if lessons == '' else lessons)
            regenerate_all_lesson = True if input('Regenerate all lesson? y/n (default n):') == 'y' else False
            if not regenerate_all_lesson:
                regenerate_id = int(input('Regenerate lesson id:'))
        except ValueError:
            print('Not a number')
        for lesson_id in lessons_id:
            generate_cards(level, lesson_id, regenerate_id, regenerate_all_lesson, american_accent, british_accent)
