from flask import Flask, jsonify

import random


def generate_job_applicants(n):
    applicants = []
    first_names = ["Иван", "Александр", "Максим", "Андрей", "Дмитрий", "Екатерина"]
    last_names = ["Смирнов", "Иванов", "Кузнецов", "Соколов", "Попова", "Морозова"]
    middle_names = ["Иванович", "Сергеевна", "Дмитриевич", "Максимовна", "Андреевич"]
    universities = ["Московский государственный университет", "Санкт-Петербургский государственный университет",
                    "Национальный исследовательский университет ИТМО", "Московский физико-технический институт",
                    "Новосибирский государственный университет", "Уральский федеральный университет"]
    faculties = ["Факультет математики и механики", "Факультет физической культуры", "Факультет иностранных языков",
                 "Факультет экономики и управления", "Факультет информационных технологий",
                 "Факультет естественных наук"]
    companies = ["Компания А", "Компания Б", "Компания В", "Компания Г", "Компания Д"]
    positions = ['Строитель', 'Водитель', 'Пилот']
    titles = ['Начинающий специалист', 'Опытный специалист']
    areas = ['Москва', "СПб", "Новосибирск"]
    industries = ["Благоустройство и уборка территорий и зданий",
                  "Земледелие, растениеводство, животноводство",
                  "Интернет-компания (поисковики, платежные системы, соц.сети)"]

    for i in range(n):
        gender_id = random.choice(['male', 'female'])
        gender_name = 'Мужской' if gender_id == 'male' else 'Женский'
        job_search_id = random.choice(['active_search', 'not_searching'])
        job_search_name = 'В активном поиске' if job_search_id == 'active_search' else 'Не ищет'
        applicant = {
            "id": i + 1,
            "title": random.choice(titles),
            "url": f"localhost:5000/{i + 1}",
            "first_name": random.choice(first_names),
            "last_name": random.choice(last_names),
            "middle_name": random.choice(middle_names),
            "can_view_full_info": True,
            "alternate_url": f"localhost:5000/{i + 1}",
            "created_at": "2015-02-06T12:00:00+0300",
            "updated_at": "2015-02-06T12:00:00+0300",
            "area": {
                "id": i + 1,
                "name": random.choice(areas),
                "url": f"https://api.hh.ru/areas/{i + 1}"
            },
            "certificate": [{
                "achieved_at": "2015-01-01",
                "owner": None,
                "title": "тест",
                "type": "custom",
                "url": "http://example.com/"
            }],
            "education": {
                "primary":
                    [{
                        "level": random.choice(["Высшее", "Среднее специальное"]),
                        "university": random.choice(universities),
                        "faculty": random.choice(faculties)
                    }
                        for _ in range(random.randint(1, 3))
                    ]},
            "total_experience": {
                "months": random.randint(0, 120)
            },
            "experience": [
                {
                    "position": random.choice(positions),
                    "start": "2010-01-01",
                    "end": None,
                    "company": random.choice(companies),
                    "industries": [
                        {
                            "id": random.randint(0, 100),
                            "name": random.choice(industries)
                        }
                        for _ in range(random.randint(1, 4))
                    ]
                }
                for _ in range(random.randint(1, 3))
            ],
            "gender": {
                "id": gender_id,
                "name": gender_name
            },
            "salary": {
                "amount": random.randint(14999, 189999),
                "currency": random.choice(['RUR', 'USD', 'EUR', 'GBP', 'JPY'])
            },
            "job_search_status": {
                "id": job_search_id,
                "name": job_search_name
            }
        }

        applicants.append(applicant)

    return applicants


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
applicants = generate_job_applicants(10)


@app.route('/resumes', methods=['GET'])
def search():
    response = {
        "found": 100,
        "per_page": 20,
        "page": 0,
        "pages": 5,
        "items": applicants,
        "platform": {
            "id": "headhunter"
        }
    }
    return jsonify(response)


@app.route('/resumes/<int:applicant_id>', methods=['GET'])
def get_applicant_by_id(applicant_id):
    for applicant in applicants:
        if applicant['id'] == applicant_id:
            return jsonify(applicant)
