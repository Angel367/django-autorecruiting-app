from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import (Model)


class CustomUser(AbstractUser):
    is_HR = models.BooleanField(default=False)
    is_HRBP = models.BooleanField(default=False)
    is_Customer = models.BooleanField(default=False)
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
INTERVIEW_STATUS_CHOICES = [
    (0, 'Назначено'),
    (1, 'Проведено успешно'),
    (2, 'Отказ')
]
TEST_TASK_STATUS_CHOICES = [
    (0, 'Отправлено кандидату'),
    (1, 'На проверке'),
    (2, 'Принято'),
    (3, 'Отказ'),
]
CANDIDATE_STATUS_CHOICES = [
    (0, 'Не выбран'),
    (1, 'Выбран'),
    (2, 'Тестовое задание'),
    (3, 'Интервью c hr'),
    (4, 'Техническое интревью'),
    (5, 'Выслан оффер'),
    (6, 'Отказ'),  # До какого момента отслеживается кандидат?
]


class VisitedCandidate(models.Model):
    idExternalService = models.IntegerField()


class Speciality(models.Model):
    specialityName = models.CharField(max_length=127)

    def __str__(self):
        return self.specialityName


class Country(models.Model):
    countryName = models.CharField(max_length=31)

    def __str__(self):
        return self.countryName


class City(models.Model):
    cityName = models.CharField(max_length=31)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.cityName + ', ' + self.country.__str__()


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


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
    isArchived = models.BooleanField(default=False)  # заменить на статус
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    testTaskDescription = models.TextField()
    testTaskLink = models.CharField(max_length=127)


class Candidate(models.Model):
    # testTask = models.ForeignKey(TestTask, on_delete=models.SET_NULL, null=True)
    # interviewHR = models.ForeignKey(Interview, on_delete=models.SET_NULL, null=True)
    # interviewCustomer = models.ForeignKey(Interview, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=CANDIDATE_STATUS_CHOICES, default=0)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    # рекомендация
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)
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
    educationLevel = models.IntegerField(choices=EDUCATION_CHOICES)


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


class Interview(models.Model):
    comment = models.TextField()
    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=datetime(1970, 1, 1))
    interviewer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=CANDIDATE_STATUS_CHOICES, default=CANDIDATE_STATUS_CHOICES)

    def set_accepted(self, comment):
        self.status = 1
        self.comment = comment
        if self.interviewer.is_Customer:
            self.candidate.status = 5  # выслать оффер
        else:
            self.candidate.status = 4

    def set_not_accepted(self, comment):
        self.status = 2
        self.comment = comment
        self.candidate.status = 6

    def get_interview_date(self):
        return self.date.strftime("%Y-%m-%d")


class TestTask(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True)
    task = models.TextField()
    link = models.CharField(max_length=255)
    startDate = models.DateTimeField(auto_now_add=True)
    finishDate = models.DateTimeField(default=datetime(1970, 1, 1))
    status = models.IntegerField(choices=TEST_TASK_STATUS_CHOICES)
    comment = models.TextField()

    def set_accepted(self, comment):
        self.status = 2
        self.comment = comment
        self.candidate.status = 3

    def set_not_accepted(self, comment):
        self.status = 3
        self.comment = comment
        self.candidate.status = 6

    def set_on_checking(self):
        self.status = 1  # на проверке -> уведомление к customer для оценки
        # если не прислано и неверно сделано -> отказ 3
        # иначе 2

    def __init__(self, finish, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task = self.candidate.vacancy.testTaskDescription
        self.link = self.candidate.vacancy.testTaskLink
        self.finishDate = finish
        self.status = 0
        self.candidate.status = 2
        now = datetime.now()
        self.startDate = now
        delay = (finish - now).total_seconds()
        s.enter(delay=delay, priority=1, action=self.set_on_checking)
