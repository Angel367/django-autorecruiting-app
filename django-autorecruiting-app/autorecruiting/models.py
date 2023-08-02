import sched
import time
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import (Model)

s = sched.scheduler(time.time, time.sleep)


class CustomUser(AbstractUser):
    is_HR = models.BooleanField(default=False)
    is_HRBP = models.BooleanField(default=False)
    is_Customer = models.BooleanField(default=False)
    patronymic = models.CharField(max_length=31, blank=True)
    phone = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.last_name + self.first_name + self.patronymic


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
    nameOfCompany = models.CharField(max_length=31)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)


class HRBP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class HR(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    hRBP = models.ForeignKey(HRBP, on_delete=models.CASCADE, null=True, blank=True)


class Vacancy(models.Model):
    chosenLetter = models.TextField()

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

    testTaskDescription = models.TextField()
    testTaskLink = models.CharField(max_length=127)
    testTaskLetter = models.TextField()


class Candidate(models.Model):
    # vacancies = models.ManyToManyField(Vacancy,  null=True)

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
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

    def __init__(self, body, sender=None, subject="", recipient=None, name="", email="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subject = subject
        self.body = body
        self.recipient = recipient
        self.name = name
        self.email = email
        self.sender = sender

        # send_mail(
        #     body=body
        #     subject=subject,
        #     sender.email,
        #     recipient.email,
        #     fail_silently=False
        # )

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']


class Interview(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(default=datetime(1970, 1, 1))
    interviewer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=CANDIDATE_STATUS_CHOICES, default=CANDIDATE_STATUS_CHOICES)

    def __init__(self, interviewer, date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = date
        self.interviewer = interviewer
        self.status = 0
        if self.interviewer.is_Customer:
            vac = VacancyCandidate.objects.get(interviewCustomer=self).get_vacancy()
            candidate = VacancyCandidate.objects.get(interviewCustomer=self).get_candidate()
            type = 'Техническое собеседование'
        else:
            vac = VacancyCandidate.objects.get(interviewHR=self).get_vacancy()
            candidate = VacancyCandidate.objects.get(interviewHR=self).get_candidate()
            type = 'Собеседование с hr'
        Message(email=candidate.email,
                name=candidate.name,
                sender=self.interviewer,
                body=f"Назначено {type} кандидату "
                     f"{candidate.name} {candidate.surname}"
                     f"по вакансии {vac.get_name()}."
                     f"День интервью: {self.date}.",
                subject=f"Назначено {type}  c {self.interviewer}"
                        f"{vac.get_name()}").save()

    def set_accepted(self, comment):
        self.status = 1
        self.comment = comment
        if self.interviewer.is_Customer:
            vac = VacancyCandidate.objects.get(interviewCustomer=self).get_vacancy()
            candidate = VacancyCandidate.objects.get(interviewCustomer=self).get_candidate()
            type = 'Техническое собеседование'
        else:
            vac = VacancyCandidate.objects.get(interviewHR=self).get_vacancy()
            candidate = VacancyCandidate.objects.get(interviewHR=self).get_candidate()
            type = 'Собеседование с hr'
        Message(email=candidate.email,
                name=candidate.name,
                sender=self.interviewer,
                body=f"{type} с кандидатом"
                     f"{candidate.name} {candidate.surname}"
                     f"по вакансии {vac.get_name()}"
                     f"по следующей причине: {comment}",
                subject=f"Успешное Интервью по вакансии "
                        f"{vac.get_name()}").save()
        if self.interviewer.is_Customer:
            VacancyCandidate.objects.get(interviewCustomer=self).send_offer(self.interviewer)


    def set_not_accepted(self, comment):
        self.status = 2
        self.comment = comment

        if self.interviewer.is_Customer:
            VacancyCandidate.objects.get(interviewCustomer=self).set_status(6)
            vac = VacancyCandidate.objects.get(interviewCustomer=self).get_vacancy()
            candidate = VacancyCandidate.objects.get(interviewCustomer=self).get_candidate()
            type = 'Техническое собеседование'
        else:
            VacancyCandidate.objects.get(interviewHR=self).set_status(6)
            vac = VacancyCandidate.objects.get(interviewHR=self).get_vacancy()
            candidate = VacancyCandidate.objects.get(interviewHR=self).get_candidate()
            type = 'Собеседование с hr'
        Message(email=candidate.email,
                name=candidate.name,
                sender=self.interviewer,
                body=f"{type} с кандидатом"
                     f"{candidate.name} {candidate.surname}"
                     f"по вакансии {vac.get_vacancy().get_name()}"
                     f"по следующей причине: {comment}",
                subject=f"Отказ Интервью по вакансии "
                        f"{vac.get_name()}").save()

    def get_interview_date(self):
        return self.date.strftime("%Y-%m-%d")


class TestTask(models.Model):
    letter_for_candidate = models.TextField()
    task = models.TextField()
    link = models.CharField(max_length=255)
    startDate = models.DateTimeField(auto_now_add=True)
    finishDate = models.DateTimeField(default=datetime(1970, 1, 1))
    status = models.IntegerField(choices=TEST_TASK_STATUS_CHOICES, default=0)
    comment = models.TextField(default="Комментарий не оставлен")

    def set_accepted(self, comment):
        self.status = 2
        self.comment = comment
        candidate = VacancyCandidate.objects.get(testTask=self).get_candidate()
        customer = HRBP.objects.get(
            vacancy=VacancyCandidate.objects.get(testTask=self).get_vacancy()
        ).get_customer()
        Message(email=candidate.email,
                name=candidate.name,
                sender=customer,
                body=f"Принято тестовое задание от кандидата "
                     f"{candidate.name} {candidate.surname}"
                     f"по вакансии {VacancyCandidate.objects.get(testTask=self).get_vacancy().get_name()}"
                     f"по следующим комментарием: {comment}",
                subject=f"Принято Тестовое задание по вакансии "
                        f"{VacancyCandidate.objects.get(testTask=self).get_vacancy().get_name()}").save()

    def set_not_accepted(self, comment):
        self.status = 3
        self.comment = comment
        VacancyCandidate.objects.get(testTask=self).set_status(6)
        candidate = VacancyCandidate.objects.get(testTask=self).get_candidate()
        customer = HRBP.objects.get(
            vacancy=VacancyCandidate.objects.get(testTask=self).get_vacancy()
        ).get_customer()
        Message(email=candidate.email,
                name=candidate.name,
                sender=customer,
                body=f"Не принято тестовое задание от кандидата "
                     f"{candidate.name} {candidate.surname}"
                     f"по вакансии {VacancyCandidate.objects.get(testTask=self).get_vacancy().get_name()}"
                     f"по следующей причине: {comment}",
                subject=f"Отказ Тестовое задание по вакансии "
                        f"{VacancyCandidate.objects.get(testTask=self).get_vacancy().get_name()}").save()

    def set_on_checking(self):
        candidate = VacancyCandidate.objects.get(testTask=self).get_candidate()
        customer = HRBP.objects.get(
            vacancy=VacancyCandidate.objects.get(testTask=self).get_vacancy()
        ).get_customer()
        Message(email=candidate.email,
                name=candidate.name,
                recipient=customer,
                body=f"Время на выполнение тестового задания вышло "
                     f"для кандидата {candidate.name} {candidate.surname}"
                     f"по вакансии {VacancyCandidate.objects.get(testTask=self).get_vacancy().get_name()}",
                subject=f"На проверку Тестовое задание по вакансии "
                        f"{VacancyCandidate.objects.get(testTask=self).get_vacancy().get_name()}").save()
        self.status = 1  # на проверке -> уведомление к customer для оценки
        # если не прислано и неверно сделано -> отказ 3
        # иначе 2

    def __init__(self, description, letter, link, finish, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.letter_for_candidate = letter
        self.task = description
        self.link = link
        self.finishDate = finish
        now = datetime.now()
        self.startDate = now
        delay = (finish - now).total_seconds()
        s.enter(delay=delay, priority=1, action=self.set_on_checking)
        candidate = VacancyCandidate.objects.get(testTask=self).get_candidate()
        hr = HR.objects.get(
            vacancy=VacancyCandidate.objects.get(testTask=self).get_vacancy()
        )
        if not hr:
            hr = HRBP.objects.get(
                vacancy=VacancyCandidate.objects.get(testTask=self).get_vacancy()
            )

        Message(email=candidate.email,
                name=candidate.name,
                sender=hr,
                body=f"Отправлено тестовое задание кандидату "
                     f"{candidate.name} {candidate.surname}"
                     f"по вакансии {VacancyCandidate.objects.get(testTask=self).get_vacancy().get_name()}."
                     f"День отправления: {self.startDate}. Дедлайн: {self.finishDate}."
                     f"Пояснение к тз: {self.letter_for_candidate}",
                subject=f"Отправлено Тестовое задание по вакансии "
                        f"{VacancyCandidate.objects.get(testTask=self).get_vacancy().get_name()}").save()


class VacancyCandidate(models.Model):
    status = models.IntegerField(choices=CANDIDATE_STATUS_CHOICES, default=0)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.SET_NULL, null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True)
    interviewHR = models.ForeignKey(Interview, on_delete=models.SET_NULL, null=True, related_name="interviewHR")
    interviewCustomer = models.ForeignKey(Interview, on_delete=models.SET_NULL, null=True,
                                          related_name="interviewCustomer")
    testTask = models.ForeignKey(TestTask, on_delete=models.SET_NULL, null=True)

    def send_offer(self, customer):
        self.status = 5
        Message(email=self.candidate.email,
                name=self.candidate.name,
                sender=customer,
                body=f"Вы приняты на работу",
                subject=f"Оффер по вакансии {self.vacancy.get_name()}").save()

    def set_interview(self, interviewer, date):
        self.interviewCustomer = Interview(interviewer=interviewer, date=date)
        if interviewer.CustomUser.is_Customer:
            self.status = 4
        else:
            self.status = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = 1
        hr = HR.objects.get(vacancy=self.vacancy)
        if not hr:
            hr = HRBP.objects.get(vacancy=self.vacancy)
        Message(email=self.candidate.email,
                name=self.candidate.name,
                sender=hr,
                body=f"Вы,{self.candidate.name} {self.candidate.surname}, выбраны кандидатом"
                     f"на вакансию {VacancyCandidate.objects.get(testTask=self).get_vacancy().get_name()}."
                     f"{self.vacancy.chosenLetter}",
                subject=f"Ответ на отклик по вакансии "
                        f"{VacancyCandidate.objects.get(testTask=self).get_vacancy().get_name()}").save()

    def set_test_task(self, finish):
        self.testTask = TestTask(
            self.vacancy.testTaskDescription,
            self.vacancy.testTaskLetter,
            self.vacancy.testTaskLink,
            finish)
        self.testTask.save()
        self.status = 2
