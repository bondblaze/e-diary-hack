import sys
import random

from random import choice
from datacenter.models import *


def fix_marks(child):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=child)
        Mark.objects.filter(schoolkid=schoolkid, points__in=[1, 2, 3]).update(points=random.randint(4, 5))
        print("Все плохие оценки исправлены.")
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников с именем {child}.", file=sys.stderr)
    except Schoolkid.DoesNotExist:
        print(f"Ученик {child} не найден.", file=sys.stderr)


def remove_chastisements(child):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=child)
        Chastisement.objects.filter(schoolkid=schoolkid).delete()
        print("Все замечания удалены.")
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников с именем {child}.", file=sys.stderr)
    except Schoolkid.DoesNotExist:
        print(f"Ученик {child} не найден.", file=sys.stderr)


def create_commendation(child, subject):
    commendations_list = [
        "Молодец!",
        "Отлично!",
        "Хорошо!",
        "Гораздо лучше, чем я ожидал!",
        "Великолепно!",
        "Прекрасно!",
        "Я тобой горжусь!",
        "Сказано здорово – просто и ясно!",
        "Очень хороший ответ!",
        "Талантливо!",
        "Я поражен!",
        "Потрясающе!",
        "Замечательно!",
        "Так держать!",
        "Ты на верном пути!",
        "Здорово!",
        "Это как раз то, что нужно!",
        "С каждым разом у тебя получается всё лучше!",
        "Мы с тобой не зря поработали!",
        "Я вижу, как ты стараешься!",
        "Ты растешь над собой!",
        "Теперь у тебя точно все получится!"
    ]

    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=child)
        latest_lesson = Lesson.objects.filter(group_letter=schoolkid.group_letter,
                                              year_of_study=schoolkid.year_of_study,
                                              subject__title=subject).order_by('-date').first()
        if latest_lesson is None:
            raise Lesson.DoesNotExist

        Commendation.objects.create(schoolkid=schoolkid, teacher=latest_lesson.teacher, subject=latest_lesson.subject,
                                    created=latest_lesson.date,
                                    text=choice(commendations_list))

        print(f"Похвала добавлена от учителя {latest_lesson.teacher}.")

    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников с именем {child}.", file=sys.stderr)
    except Schoolkid.DoesNotExist:
        print(f"Ученик {child} не найден.", file=sys.stderr)
    except Lesson.DoesNotExist:
        print(f"Предмет {subject} не найден.", file=sys.stderr)
