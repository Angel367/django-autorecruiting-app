import base64
import io
import json

import matplotlib.pyplot as plt
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import redirect
from django.shortcuts import render
from .test_data_create import on_start_function

from .models import *


def index(request):
    return render(request, 'index.html')


@login_required
def candidates(request):
    context = {
        'candidates': Candidate.objects.all(),
        'cities': City.objects.all(),
        'specialities': Speciality.objects.all(),
        'vacancies': get_all_vacancies_by_hr_or_hrbp_id(request.user.id, )
    }
    return render(request, 'candidates.html', context=context)


@login_required
def find_candidates(request):
    context = {
        'specialities': Speciality.objects.all(),
        'cities': City.objects.all(),
        'vacancies': get_all_vacancies_by_hr_or_hrbp_id(request.user.id)
    }
    if 'find' in request.POST:
        candidates_list = Candidate.objects.all()
        print(candidates_list.count())
        main_vacancy = Vacancy()
        if request.POST.get('main_vacancy_id') != "":
            main_vacancy = Vacancy.objects.get(id=request.POST.get('main_vacancy_id'))
        print(main_vacancy)
        if request.POST.get('speciality') != "":
            candidates_list = candidates_list.filter(speciality=request.POST.get('speciality'))
            main_vacancy.speciality_id = request.POST.get('speciality')
        else:
            main_vacancy.speciality.specialityName = ""
        print(candidates_list.count())
        print(main_vacancy)
        if request.POST.get('city') != "":
            candidates_list = candidates_list.filter(city=request.POST.get('city'))
            main_vacancy.city_id = City.objects.get(id=request.POST.get('city'))
        else:
            main_vacancy.city.cityName = ""
        print(candidates_list.count())
        if request.POST.get('workExperienceFrom') != "":
            candidates_list = candidates_list.filter(
                vacancy__workExperienceFrom__range=(request.POST.get('workExperienceFrom'), 100000000000000))
            main_vacancy.workExperienceFrom = request.POST.get('workExperienceFrom')
        else:
            main_vacancy.workExperienceFrom = 100000000000000
        print(candidates_list.count())
        if request.POST.get('workExperienceTo') != "":
            candidates_list = candidates_list.filter(
                vacancy__workExperienceTo__range=(0, request.POST.get('workExperienceTo')))
            main_vacancy.workExperienceTo = request.POST.get('workExperienceTo')
        else:
            main_vacancy.workExperienceTo = 0
        print(candidates_list.count())
        if request.POST.get('suggestedSalaryFrom') != "":
            candidates_list = candidates_list.filter(
                vacancy__suggestedSalaryFrom__range=(request.POST.get('suggestedSalaryFrom'), 100000000000000))
            main_vacancy.suggestedSalaryFrom = request.POST.get('suggestedSalaryFrom')
        else:
            main_vacancy.suggestedSalaryFrom = 0
        if request.POST.get('suggestedSalaryTo') != "":
            main_vacancy.suggestedSalaryTo = request.POST.get('suggestedSalaryTo')
            candidates_list = candidates_list.filter(
                vacancy__suggestedSalaryTo__range=(0, request.POST.get('suggestedSalaryTo')))
        else:
            main_vacancy.suggestedSalaryTo = 100000000000000
        context.update({'candidates': candidates_list})
        context.update({'main_vacancy': main_vacancy})

    return render(request, 'candidates.html', context=context)


@login_required
def candidates_by_vacancy_id(request, id):
    context = {
        'main_vacancy': Vacancy.objects.get(id=id),
        'specialities': Speciality.objects.all(),
        'candidates': Candidate.objects.all(),
        'cities': City.objects.all(),
        'vacancies': get_all_vacancies_by_hr_or_hrbp_id(request.user.id)
    }
    return render(request, 'candidates.html', context=context)


@login_required
def candidate_information_messenger(request, id):
    context = {
        'candidate': Candidate.objects.get(id=id),
        'CANDIDATE_STATUS_CHOICES': dict(CANDIDATE_STATUS_CHOICES)
    }
    return render(request, 'candidate-information-messenger.html', context=context)


@login_required
def candidate_information_main(request, id):
    if request.method == 'POST':
        if request.POST.get('status') is not None:
            new_status = request.POST.get('status')
            candidate = Candidate.objects.get(id=id)
            candidate.status = new_status
            candidate.save()
        else:
            candidate = Candidate.objects.get(id=id)
            candidate.interviewerFullName = request.POST.get('interviewerFullName')
            candidate.interviewDate = request.POST.get('interviewDate')
            candidate.save()
    context = {
        'candidate': Candidate.objects.get(id=id),
        'CANDIDATE_STATUS_CHOICES': dict(CANDIDATE_STATUS_CHOICES)
    }
    visited = VisitedCandidate(idExternalService=id)
    visited.save()
    return render(request, 'candidate-information-main.html', context=context)


def candidate_information(request):
    return render(request, 'candidate-information.html', {'messages': get_user_messages_json("arinka", "asdfwe")})


# доступен только hrbp
@login_required()
def hr_all(request):
    try:
        target_hrbp_id = HRBP.objects.get(user_id=request.user.id).id
    except:
        return HttpResponseForbidden()
    context = {
        'hrs': get_all_hrs_of_hrbp(target_hrbp_id)
    }
    return render(request, 'hr-all.html', context=context)


def get_all_hrs_of_hrbp(target_hrbp_id):
    return HR.objects.filter(hRBP_id=target_hrbp_id)


def get_all_vacancies_by_hr_or_hrbp_id(hr_bp_id, is_archived=False):
    user = CustomUser.objects.get(id=hr_bp_id)
    if user.is_HR:
        print(user.username, user.hr.hRBP_id)
    if user.is_HR:
        target_hr = HR.objects.get(user_id=hr_bp_id)
        print(target_hr.user.username)
        return Vacancy.objects.filter(hR_id=target_hr, isArchived=is_archived)
    elif user.is_HRBP:
        target_hrbp = HRBP.objects.get(user_id=hr_bp_id)
        return Vacancy.objects.filter(hRBP_id=target_hrbp.id, isArchived=is_archived)


@login_required
def hr_vacancies(request):
    context = {
        'vacancies': get_all_vacancies_by_hr_or_hrbp_id(request.user.id)
    }
    return render(request, 'hr-vacancies.html', context=context)


# доступен только hrbp
@login_required
def hr_own_vacancies(request, id):
    context = {
        'hr': HR.objects.get(id=id),
        'vacancies': get_all_vacancies_by_hr_or_hrbp_id(HR.objects.get(id=id).user_id)
    }
    return render(request, 'hr-own-vacancies.html', context=context)


@login_required
def hr_archive_vacancies(request):
    context = {
        'vacancies': get_all_vacancies_by_hr_or_hrbp_id(request.user.id, True)
    }
    return render(request, 'hr-vacancies.html', context=context)


@login_required
def hr_messenger(request):
    context = {

    }
    return render(request, 'hr-messenger.html', context=context)


# TODO Аделина сделай нормальный css и html для этой страницы спасибо большое
@login_required
def hr_statistics(request):
    user = request.user
    if user.is_HR:
        target_hr = HR.objects.get(user_id=user.id)
    elif user.is_HRBP:
        target_hr = HRBP.objects.get(user_id=user.id)
    all_candidates_with_status, labels = [], []
    for i in range(len(CANDIDATE_STATUS_CHOICES)):
        if user.is_HR:
            all_candidates_with_status.append(Candidate.objects.filter(vacancy__hR=target_hr, status=i).count())
        elif user.is_HRBP:
            all_candidates_with_status.append(Candidate.objects.filter(vacancy__hR__hRBP=target_hr, status=i).count())
        labels.append(CANDIDATE_STATUS_CHOICES[i][1])
    print(all_candidates_with_status)
    plt.pie(all_candidates_with_status, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()

    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plot_data = base64.b64encode(image_stream.getvalue()).decode()
    plt.close()
    # plt.show()

    Candidate.objects.filter()

    context = {
        'user': request.user,
        'plot_data': plot_data
    }
    return render(request, 'hr-statistics.html', context=context)


@login_required
def vacancy_edit_add(request):
    if 'save' in request.POST:
        if not request.POST.get('id'):
            vacancy = Vacancy(name=request.POST.get('name'),
                              employmentType=request.POST.get('employmentType'),
                              workSchedule=request.POST.get('workSchedule'),
                              vacancyDescription=request.POST.get('vacancyDescription'),
                              workExperienceFrom=request.POST.get('workExperienceFrom'),
                              workExperienceTo=request.POST.get('workExperienceTo'),
                              suggestedSalaryFrom=request.POST.get('suggestedSalaryFrom'),
                              suggestedSalaryTo=request.POST.get('suggestedSalaryTo'),
                              educationLevel=request.POST.get('educationLevel'),
                              city_id=request.POST.get('city'),
                              speciality_id=request.POST.get('speciality')
                              )
            if request.user.is_HRBP:
                vacancy.hRBP = HRBP.objects.get(user_id=request.user.id)
                if request.POST.get('hR') != '':
                    vacancy.hR = HR.objects.get(id=request.POST.get('hR'))
            else:
                vacancy.hR = HR.objects.get(user_id=request.user.id)
                vacancy.hRBP = HRBP.objects.get(id=request.user.hr.hRBP_id)
        else:
            vacancy = Vacancy.objects.get(id=request.POST.get('id'))
            vacancy.name = request.POST.get('name')
            vacancy.city_id = request.POST.get('city')
            if request.user.is_HRBP and request.POST.get('hR') != '':
                vacancy.hR = HR.objects.get(id=request.POST.get('hR'))
            vacancy.employmentType = request.POST.get('employmentType')
            vacancy.speciality_id = request.POST.get('speciality')
            vacancy.workSchedule = request.POST.get('workSchedule')
            vacancy.vacancyDescription = request.POST.get('vacancyDescription')
            vacancy.workExperienceFrom = request.POST.get('workExperienceFrom')
            vacancy.workExperienceTo = request.POST.get('workExperienceTo')
            vacancy.suggestedSalaryFrom = request.POST.get('suggestedSalaryFrom')
            vacancy.suggestedSalaryTo = request.POST.get('suggestedSalaryTo')
            vacancy.educationLevel = request.POST.get('educationLevel')
        vacancy.save()
    if 'archive_out' in request.POST:
        vacancy = Vacancy.objects.get(id=request.POST.get('id'))
        vacancy.isArchived = False
        vacancy.save()
    if 'archive_into' in request.POST:
        vacancy = Vacancy.objects.get(id=request.POST.get('id'))
        vacancy.isArchived = True
        vacancy.save()
    return HttpResponseRedirect('/vacancy-information/' + vacancy.id.__str__())


@login_required
def edit_vacancy(request, id):
    context = {
        'EMPLOYMENT_TYPE_CHOICES': dict(EMPLOYMENT_TYPE_CHOICES),
        'EDUCATION_CHOICES': dict(EDUCATION_CHOICES),
        'WORK_SCHEDULE_CHOICES': dict(WORK_SCHEDULE_CHOICES),
        'cities': City.objects.all().order_by('country_id'),
        'vacancy': Vacancy.objects.get(id=id),
        'specialities': Speciality.objects.all()
    }
    if request.user.is_HRBP:
        context.update({'hrs': HRBP.objects.get(user_id=request.user.id).hr_set.all()})
    return render(request, 'vacancy-edit-or-add.html', context=context)


@login_required
def add_vacancy(request):
    context = {
        'EMPLOYMENT_TYPE_CHOICES': dict(EMPLOYMENT_TYPE_CHOICES),
        'EDUCATION_CHOICES': dict(EDUCATION_CHOICES),
        'WORK_SCHEDULE_CHOICES': dict(WORK_SCHEDULE_CHOICES),
        'cities': City.objects.all().order_by('country_id'),
        'specialities': Speciality.objects.all()
    }
    if request.user.is_HRBP:
        context.update({'hrs': HRBP.objects.get(user_id=request.user.id).hr_set.all()})
    return render(request, 'vacancy-edit-or-add.html', context=context)


@login_required
def add_hr(request):
    return render(request, 'hr-edit-or-add.html')


@login_required
def hr_edit_add(request):
    print('stopped here')
    # if 'save' in request.POST:
    #     if not request.POST.get('id'):
    #         if request.user.isHRBP:
    #         hr = HR(username=request.POST.get(''),
    #
    #                 )


#  arg user.id
@login_required
def edit_hr_by_id(request, id):
    if request.user.is_HR:
        hr = HR.objects.get(user_id=request.user.id)
    else:
        if request.user.id == id:
            hr = HRBP.objects.get(user_id=id)
        else:
            hr = HR.objects.get(user_id=id)

    context = {
        'hr': hr
    }
    return render(request, 'hr-edit-or-add.html', context=context)


def search_resumes(request):
    response = requests.get(url='http://127.0.0.1:5000/resumes')
    resumes_json = response.json()
    resumes = resumes_json['items']
    return render(request, 'search-resumes.html', {'resumes': resumes})


@login_required
def vacancy_information(request, id):
    vacancy = Vacancy.objects.filter(id=id)[0]

    context = {
        'vacancy': vacancy,
        'candidates': Candidate.objects.filter(vacancy_id=vacancy.id)
    }
    return render(request, 'vacancy-information.html', context=context)


# User = get_user_model()
#
# def send_message(request):
#     if request.method == 'POST':
#         sender = get_object_or_404(User, id=request.POST['sender_id'])
#         recipient = get_object_or_404(User, id=request.POST['recipient_id'])
#         message_body = request.POST['message_body']
#         message = MessageModel.objects.create(user=sender, recipient=recipient, body=message_body)
#         message.save()
#         return JsonResponse({"message": "message sent successfully."}, status=201)
#     else:
#         return JsonResponse({"error": "Invalid method."}, status=400)
#
# def get_messages(request, user_id, recipient_id):
#     if request.method == 'GET':
#         user = get_object_or_404(User, id=user_id)
#         recipient = get_object_or_404(User, id=recipient_id)
#         messages = MessageModel.objects.filter(user=user, recipient=recipient)
#         messages_list = list(messages.values())
#         return JsonResponse(messages_list, safe=False)
#     else:
#         return JsonResponse({"error": "Invalid method."}, status=400)


def message_list(request):
    if request.user.is_HR:
        recipient = request.user.hr.hRBP
    messages = MessageModel.objects.filter(user=request.user, recipient=recipient)
    return render(request, 'hr-messenger.html', {'messages': messages, 'recipient': recipient})


# def register_page(request):
#     return render(request, 'register_page.html')

def send_message(request):
    message = MessageModel(user=get_user(json.loads(request.body)["user"]),
                           recipient=get_user(json.loads(request.body)["recipient"]),
                           body=json.loads(request.body)["body"])
    message.save()
    return JsonResponse({'message': 'success'})


#
# @csrf_exempt
# def create_user(request):
#     if request.method == 'POST':
#         username = json.loads(request.body)["username"]
#         password = json.loads(request.body)["password"]
#         if username and password:
#             try:
#                 user = User.objects.get(username=username)
#                 return JsonResponse({'error': 'User already exists.'}, status=400)
#             except ObjectDoesNotExist:
#                 user = User.objects.create_user(username, password=password)
#                 print("created")
#                 return JsonResponse({'success': 'User created successfully.'}, status=200)
#         else:
#             return JsonResponse({'error': 'Missing username or password.'}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request.'}, status=400)


def get_user(username):
    try:
        user = CustomUser.objects.get(username=username)
        print(username)
        return user
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)


from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import MessageModel


def get_user_messages(request, username):
    """
    Returns a JSON response with all messages where the given user is either the sender or the recipient.
    """
    try:
        user = get_user(username=username)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    user_messages = MessageModel.objects.filter(Q(user=user) | Q(recipient=user))

    message_list = []
    for message in user_messages:
        is_recipient = (message.recipient == user)
        message_list.append({
            "body": message.body,
            "timestamp": message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "is_recipient": is_recipient
        })

    return JsonResponse(message_list, safe=False)


def get_user_messages_json(username, recipient):
    """
    Returns a JSON response with all messages where the given user is either the sender or the recipient.
    """
    try:
        user = get_user(username=username)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    try:
        recipient = get_user(username=recipient)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    user_messages = MessageModel.objects.filter(Q(user=user) and Q(recipient=recipient))

    message_list = []
    for message in user_messages:
        is_recipient = (message.recipient == user)
        message_list.append({
            "body": message.body,
            "timestamp": message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "is_recipient": is_recipient
        })
    message_list.reverse()
    return message_list


def login_view(request):
    if len(CustomUser.objects.all()) == 0:
        on_start_function()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')

            if next_url:
                return redirect(next_url)
            else:
                return redirect('/hr/vacancies')  # Replace 'home' with your desired redirect URL
        else:
            error_message = "Пользователь с такими данными не найден"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
