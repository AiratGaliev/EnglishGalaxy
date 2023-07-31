from Accent import Accent
from Config import Config
from utils import generate_cards, parse_numeric_array

if __name__ == '__main__':
    level_id = Config.LEVEL_ID.value
    accent = Config.ACCENT.value
    lessons_id: list[int] = []
    regenerate_id: int = 0
    regenerate_all_lesson: bool = False
    regenerate_all_level: bool = False
    try:
        print("Lessons level is {level_id}".format(level_id=level_id.upper()))
        if accent == Accent.AMERICAN.value:
            print("An American accent has been chosen")
        if accent == Accent.BRITISH.value:
            print("A British accent has been chosen")
        lessons = input("Enter lessons in the format '1' or '1..10':")
        lessons_id = parse_numeric_array(lessons)
        regenerate_all_lesson = True if input('Regenerate all lesson? y/n (default n):') == 'y' else False
        if not regenerate_all_lesson:
            regenerate_id = int(input('Regenerate lesson id:'))
    except ValueError:
        print('Not a number')
    for lesson_id in lessons_id:
        generate_cards(level_id, lesson_id, regenerate_id, regenerate_all_lesson, accent)
