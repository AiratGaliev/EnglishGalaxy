from Config import Config
from utils import generate_cards

if __name__ == '__main__':
    level_id = Config.LEVEL_ID.value
    lesson_id: int = 0
    regenerate_id: int = 0
    regenerate_all_lesson: bool = False
    # TODO реализовать логику перегенерации всего уровня
    regenerate_all_level: bool = False
    try:
        lesson_id = int(input('Enter lesson id:'))
        regenerate_all_lesson = True if input('Regenerate all lesson? y/n (default n):') == 'y' else False
        if not regenerate_all_lesson:
            regenerate_id = int(input('Regenerate lesson id:'))
    except ValueError:
        print('Not a number')
    generate_cards('English Galaxy {level_id}'.format(level_id=level_id.upper()),
                   'Lesson_{lesson_id}'.format(lesson_id=lesson_id), level_id, lesson_id, regenerate_id,
                   regenerate_all_lesson)
    print("Done!")
