import random

from datacenter.models import (Chastisement, Commendation, Lesson, Mark, Schoolkid, Subject)

import django.core.exceptions


def get_student_by_name(student_name: str):
    try:
        target_student = Schoolkid.objects.get(full_name__contains=student_name)

        return target_student
    except django.core.exceptions.MultipleObjectsReturned:
        print(f'Multiple records for query {student_name} were found')
    except django.core.exceptions.ObjectDoesNotExist:
        print(f'No records found for query {student_name}')


def create_commendation(student: str, subject_title: str) -> bool:
    target_student = get_student_by_name(student)
    possible_commendations = ['Хвалю!', 'Молодец', 'Так держать!', 'Ты сегодня прыгнул выше головы!',
                              'Здорово!', 'Гораздо лучше, чем я ожидал!']

    if not target_student:
        return False

    student_target_lessons = Lesson.objects.filter(
        year_of_study=target_student.year_of_study,
        group_letter=target_student.group_letter,
        subject__title=subject_title
    )

    if student_target_lessons.count():
        commendation_lesson = random.choice(student_target_lessons)
        commendation_text = random.choice(possible_commendations)

        Commendation.objects.create(
            text=commendation_text,
            created=commendation_lesson.date,
            schoolkid=target_student,
            subject=commendation_lesson.subject,
            teacher=commendation_lesson.teacher
        )

        return True

    return False


def remove_chastisements(student: str):
    target_student = get_student_by_name(student)

    if not target_student:
        return False

    student_chastisements = Chastisement.objects.filter(schoolkid=target_student.id)
    student_chastisements.delete()

    return True


def fix_marks(student: str, limit=4):
    target_student = get_student_by_name(student)

    if not target_student:
        return False

    good_mark = random.choice(range(limit, 6))

    bad_marks = Mark.objects.filter(schoolkid=target_student.id, points__lt=limit)
    bad_marks.update(points=good_mark)

    return True
