import sys
import random

from random import choice
from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation

COMMENDATIONS = [
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


def find_schoolkid(child):
    try:
        return Schoolkid.objects.get(full_name__contains=child)
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников с именем {child}.", file=sys.stderr)
        exit()
    except Schoolkid.DoesNotExist:
        print(f"Ученик {child} не найден.", file=sys.stderr)
        exit()


def fix_marks(child):
    Mark.objects.filter(schoolkid=find_schoolkid(child), points__in=[1, 2, 3]).update(points=random.randint(4, 5))
    print("Все плохие оценки исправлены.")


def remove_chastisements(child):
    Chastisement.objects.filter(schoolkid=find_schoolkid(child)).delete()
    print("Все замечания удалены.")


def create_commendation(child, subject):
    try:
        latest_lesson = Lesson.objects.filter(group_letter=find_schoolkid(child).group_letter,
                                              year_of_study=find_schoolkid(child).year_of_study,
                                              subject__title=subject).order_by('-date').first()
        if latest_lesson is None:
            raise Lesson.DoesNotExist

        Commendation.objects.create(schoolkid=find_schoolkid(child), teacher=latest_lesson.teacher,
                                    subject=latest_lesson.subject,
                                    created=latest_lesson.date,
                                    text=choice(COMMENDATIONS))

        print(f"Похвала добавлена от учителя {latest_lesson.teacher}.")
    except Lesson.DoesNotExist:
        print(f"Предмет {subject} не найден.", file=sys.stderr)
        exit()
