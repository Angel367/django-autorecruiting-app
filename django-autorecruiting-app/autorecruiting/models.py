from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import User
from django.db.models import (Model, TextField, DateTimeField, ForeignKey,
                              CASCADE)
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# Create your models here.


class CustomUser(AbstractUser):
    is_HR = models.BooleanField(default=False)
    is_HRBP = models.BooleanField(default=False)
    patronymic = models.CharField(max_length=31, blank=True)
    phone = models.CharField(max_length=10, blank=True)


EMPLOYMENT_TYPE_CHOICES = [
    (0, 'Полная занятость'),
    (1, 'Стажировка'),
    (2, 'Частичная занятость'),
]

WORK_SCHEDULE_CHOICES = [
    (0, 'Полный день'),
    (1, 'Удалённая работа'),
    (2, 'Гибкий график'),
]

EDUCATION_CHOICES = [
    (0, 'Основное общее'),
    (1, 'Среднее общее'),
    (2, 'Среднее профессиональное'),
    (3, 'Неоконченное высшее'),
    (4, 'Бакалавр'),
    (5, 'Магистр'),
]

CANDIDATE_STATUS_CHOICES = [
    (0, 'Выбран'),
    (1, 'Тестовое задание выслано'),
    (2, 'Тестовое задание на проверке'),
    (3, 'Тестовое задание принято'),
    (4, 'Интервью назначено'),
    (5, 'Принят на работу'),
    (6, 'Не прошёл собеседование'),
    (7, 'Не выбран'),
    (8, 'Выслан оффер'),
]


class VisitedCandidate(models.Model):
    idExternalService = models.IntegerField()


class Speciality(models.Model):
    specialityName = models.CharField(max_length=127)


class Country(models.Model):
    countryName = models.CharField(max_length=31)


class City(models.Model):
    cityName = models.CharField(max_length=31)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Customer(models.Model):
    name = models.CharField(max_length=31)
    surname = models.CharField(max_length=31)
    patronymic = models.CharField(max_length=31, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    email = models.CharField(max_length=31)


class HRBP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class HR(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    hRBP = models.ForeignKey(HRBP, on_delete=models.CASCADE, null=True, blank=True)


class Vacancy(models.Model):
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=127)
    hR = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True)
    hRBP = models.ForeignKey(HRBP, on_delete=models.CASCADE, null=True, blank=True)
    employmentType = models.IntegerField(choices=EMPLOYMENT_TYPE_CHOICES, default=EMPLOYMENT_TYPE_CHOICES)
    workSchedule = models.IntegerField(choices=WORK_SCHEDULE_CHOICES, default=WORK_SCHEDULE_CHOICES)
    vacancyDescription = models.CharField(max_length=2047)
    workExperienceFrom = models.IntegerField(default=1)
    workExperienceTo = models.IntegerField(default=3)
    suggestedSalaryFrom = models.IntegerField(default=200000)
    suggestedSalaryTo = models.IntegerField(default=500000)
    educationLevel = models.IntegerField(choices=EDUCATION_CHOICES)
    isArchived = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)


class TestTask(models.Model):
    link = models.CharField(max_length=255)
    duration = models.IntegerField()


class Candidate(models.Model):
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)
    testTask = models.ForeignKey(TestTask, on_delete=models.SET_NULL, null=True)
    interviewDate = models.DateTimeField(default=datetime(1970, 1, 1))
    interviewerFullName = models.CharField(max_length=127, default="Интервьюер Петров")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    # рекомендация
    name = models.CharField(max_length=31)
    surname = models.CharField(max_length=31)
    patronymic = models.CharField(max_length=31, blank=True)
    email = models.CharField(max_length=31)
    phone = models.CharField(max_length=10, blank=True)
    birthdayDate = models.DateField()
    resumeLink = models.CharField(max_length=255)
    workExperienceDuration = models.IntegerField()
    relocationReady = models.BooleanField()
    expectedSalaryFrom = models.IntegerField()
    expectedSalaryTo = models.IntegerField()
    status = models.IntegerField(choices=CANDIDATE_STATUS_CHOICES, default=CANDIDATE_STATUS_CHOICES)
    educationLevel = models.IntegerField(choices=EDUCATION_CHOICES)

    def get_interview_date(self):
        return self.interviewDate.strftime("%Y-%m-%d")


class Message(Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']
