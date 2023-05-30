from datetime import date

from django import template

register = template.Library()


@register.filter
def display_months(months):
    months = int(months)
    years = months // 12
    remaining_months = months % 12

    # Формирование строки с учетом склонений
    result = ""
    if years > 0:
        result += f"{years} {'год' if years == 1 else 'года' if 2 <= years <= 4 else 'лет'}"
    elif years == 0 and remaining_months == 0:
        return "Нет опыта"
    if remaining_months > 0:
        if years > 0:
            result += " "
        result += f"{remaining_months} {'месяц' if remaining_months == 1 else 'месяца' if 2 <= remaining_months <= 4 else 'месяцев'}"

    return result


@register.filter
def display_year_interval(year_to):
    if year_to == 0:
        return "Без опыта"
    elif year_to == 1:
        return "1 год"
    elif 2 <= year_to <= 4:
        return str(year_to) + " года"
    else:
        return str(year_to) + " лет"


@register.filter
def display_age(birthday):

    today = date.today()
    age = today.year - birthday.year

    # Check if the birthday has already occurred this year
    if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
        age -= 1

    return age
