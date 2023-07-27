from datetime import datetime

from .models import *
import random


def on_start_function():
    generate_speciality()
    generate_country()
    generate_city()
    generate_customers()
    generate_users()
    generate_vacancies()
    generate_candidates()


def generate_customers(amount=5):
    for i in range(amount):
        Customer.objects.create(
            user=CustomUser.objects.create_user(
                username="Заказчик" + str(i),
                last_name="ЗаказчикФамилия" + str(i),
                first_name="ЗаказчикИмя" + str(i),
                patronymic="ЗаказчикОтчество" + str(i),
                phone="6723647198",
                email="Customer" + str(i) + "@gmail.com",
                password="12345678",
                is_Customer=True
            )
        )


def generate_country(amount=2):
    for i in range(amount):
        Country.objects.create(
            countryName="Страна" + str(i)
        )


def generate_speciality(amount=4):
    for i in range(amount):
        Speciality.objects.create(
            specialityName="Специальность" + str(i)
        )


def generate_city(amount=4):
    for i in range(amount):
        City.objects.create(
            cityName="Город" + str(i),
            country_id=random.randint(1, len(Country.objects.all()))
        )


def generate_users(amount_HR=25, amount_HRBP=5):
    for i in range(0, amount_HRBP):
        HRBP.objects.create(
            customer_id=1 + i,
            user=CustomUser.objects.create_user(
                username="HRBP" + str(i),
                last_name="HRBPФамилия" + str(i),
                first_name="HRBPИмя" + str(i),
                patronymic="HRBPОтчество" + str(i),
                phone="6723647198",
                email="HRBP" + str(i) + "@gmail.com",
                password="12345678",
                is_HRBP=True
            )
        )
    for j in range(0, amount_HR):
        HR.objects.create(
            hRBP_id=random.randint(1, len(HRBP.objects.all())),
            user=CustomUser.objects.create_user(
                username="HR" + str(j),
                last_name="HRФамилия" + str(j),
                first_name="HRИмя" + str(j),
                patronymic="HRОтчество" + str(j),
                phone="1723647198",
                email="HR" + str(j) + "@gmail.com",
                password="12345678",
                is_HR=True
            )
        )


def generate_vacancies(amount=50):
    for i in range(amount):
        vacancy = Vacancy()
        vacancy.speciality_id = random.randint(1, len(Speciality.objects.all()))
        vacancy.name = "Вакансия №" + str(i)
        vacancy.hR_id = random.randint(1, len(HR.objects.all()))  # Set HR randomly
        vacancy.hRBP_id = vacancy.hR.hRBP_id
        vacancy.employmentType = random.choice([choice[0] for choice in EMPLOYMENT_TYPE_CHOICES])
        vacancy.workSchedule = random.choice([choice[0] for choice in WORK_SCHEDULE_CHOICES])
        vacancy.vacancyDescription = "Sample vacancy description"
        work_experience_from = random.randint(0, 5)
        vacancy.workExperienceFrom = work_experience_from
        vacancy.workExperienceTo = random.randint(work_experience_from, 10)
        vacancy.suggestedSalaryFrom = random.randint(100000, 300000)  # Set salary range randomly
        vacancy.suggestedSalaryTo = random.randint(400000, 700000)
        vacancy.educationLevel = random.choice([choice[0] for choice in EDUCATION_CHOICES])
        vacancy.city_id = random.randint(1, len(City.objects.all()))  # Set City randomly
        if i % 2:
            vacancy.isArchived = True
        vacancy.save()


def generate_candidates(amount=50):
    for i in range(amount):
        c = Candidate.objects.create(
            speciality_id=random.randint(1, len(Speciality.objects.all())),
            name="CANDIDATEname" + str(i),
            surname="CANDIDATEsurname" + str(i),
            patronymic="CANDIDATEpatronymic" + str(i),
            phone="8898897767",
            workExperienceDuration=random.randint(1, 300),
            birthdayDate=datetime(2001, 5, 12),
            resumeLink="",
            relocationReady=random.randint(0, 1),
            expectedSalaryFrom=random.randint(100000, 300000),
            expectedSalaryTo=random.randint(400000, 700000),
            educationLevel=random.choice([choice[0] for choice in EDUCATION_CHOICES]),
            city_id=random.randint(1, len(City.objects.all())),
            email="CANDIDATE" + str(i) + "@gmail.com",
        )
        if Vacancy.objects.get(id=i+1) and not Vacancy.objects.get(id=i+1).isArchived:
            c.vacancy_id = i+1
            c.status = random.randint(1, 7)
        c.save()
