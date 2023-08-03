import base64
import io
from django.views.generic import CreateView
import matplotlib.pyplot as plt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import redirect
from django.shortcuts import render
from .forms import *
from .models import *
from .test_data_create import on_start_function


def index(request):
    return render(request, 'index.html')


@login_required
def candidates(request):
    context = {
        'candidates': Candidate.objects.all()[:15],
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
        if request.POST.get('id') != "":
            context.update({'id': request.POST.get('id')})
            context.update({'name': Vacancy.objects.get(id=request.POST.get('id')).name})
        if request.POST.get('speciality') != "":
            candidates_list = candidates_list.filter(speciality_id=request.POST.get('speciality'))
            context.update({'speciality': request.POST.get('speciality')})
        print(candidates_list.count())
        if request.POST.get('city') != "":
            candidates_list = candidates_list.filter(city_id=request.POST.get('city'))
            context.update({'city': request.POST.get('city')})
        print(candidates_list.count())
        if request.POST.get('workExperienceFrom') != "":
            candidates_list = candidates_list.filter(
                workExperienceDuration__range=(request.POST.get('workExperienceFrom'), 100000000000000))
            context.update({'workExperienceFrom': request.POST.get('workExperienceFrom')})
        print(candidates_list.count())
        if request.POST.get('workExperienceTo') != "":
            candidates_list = candidates_list.filter(
                workExperienceDuration__range=(0, request.POST.get('workExperienceTo')))
            context.update({'workExperienceTo': request.POST.get('workExperienceTo')})
        print(candidates_list.count())
        if request.POST.get('suggestedSalaryFrom') != "":
            candidates_list = candidates_list.filter(
                expectedSalaryFrom__range=(request.POST.get('suggestedSalaryFrom'), 100000000000000))
            context.update({'suggestedSalaryFrom': request.POST.get('suggestedSalaryFrom')})
        print(candidates_list.count())
        if request.POST.get('suggestedSalaryTo') != "":
            context.update({'suggestedSalaryTo': request.POST.get('suggestedSalaryTo')})
            candidates_list = candidates_list.filter(
                expectedSalaryTo__range=(0, request.POST.get('suggestedSalaryTo')))
        context.update({'candidates': candidates_list})
    return render(request, 'candidates.html', context=context)


@login_required
def candidates_by_vacancy_id(request, id):
    context = {
        'id': Vacancy.objects.get(id=id).id,
        'name': Vacancy.objects.get(id=id).name,
        'speciality': Vacancy.objects.get(id=id).speciality,
        'suggestedSalaryTo': Vacancy.objects.get(id=id).suggestedSalaryTo,
        'suggestedSalaryFrom': Vacancy.objects.get(id=id).suggestedSalaryFrom,
        'workExperienceTo': Vacancy.objects.get(id=id).workExperienceTo,
        'workExperienceFrom': Vacancy.objects.get(id=id).workExperienceFrom,
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
    # if '' in request.POST:

    context = {
        'vacancies': get_all_vacancies_by_hr_or_hrbp_id(request.user.id),
        'candidate': Candidate.objects.get(id=id),
        'CANDIDATE_STATUS_CHOICES': dict(CANDIDATE_STATUS_CHOICES)
    }
    visited = VisitedCandidate(idExternalService=id)
    visited.save()
    return render(request, 'candidate-information-main.html', context=context)


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
def hr_messenger_to_hrbp(request, id):
    user = CustomUser.objects.get(id=request.user.id)
    addressee = CustomUser.objects.get(id=id)
    context = {
        'addressee': addressee,
        'messages': Message.objects.filter(sender=user, recipient=addressee).order_by('created')
                    | Message.objects.filter(sender=addressee, recipient=user).order_by('created')
    }
    if 'send' in request.POST:
        message = Message(recipient=addressee, sender=user, subject=request.POST.get('subject'),
                          body=request.POST.get('body'))
        message.save()
        # send_mail(
        #     request.POST.get('subject'),
        #     request.POST.get('body'),
        #     user.email,
        #     [addressee.email],
        #     fail_silently=False,
        # )
    return render(request, 'hr-messenger.html', context=context)


@login_required
def hr_messenger_to_candidate(request, id):
    addressee = Candidate.objects.get(id=id)
    user = CustomUser.objects.get(id=request.user.id)
    messages = Message.objects.filter(sender=user, email=addressee.email).order_by('created')
    if user.is_HR:
        user1 = HRBP.objects.get(user_id=user.hRBP.user.id)
        user2 = Customer.objects.get(user_id=user1.customer.user.id)
        messages = messages | Message.objects.filter(sender=user1, email=addressee.email).order_by('created') \
                   | Message.objects.filter(sender=user2, email=addressee.email).order_by('created') \
              |  Message.objects.filter(recipient=user2, email=addressee.email).order_by('created')
    context = {
        'addressee': addressee,
        'messages': messages,
        # | Message.objects.filter(email=addressee.email, recipient=user).order_by('created')
        'candidate': Candidate.objects.get(id=id),
        'CANDIDATE_STATUS_CHOICES': dict(CANDIDATE_STATUS_CHOICES)
    }
    if 'send' in request.POST:
        message = Message(email=addressee.email, sender=user, subject=request.POST.get('subject'),
                          body=request.POST.get('body'))
        # send_mail(
        #     request.POST.get('subject'),
        #     request.POST.get('body'),
        #     user.email,
        #     [addressee.email],
        #     fail_silently=False,
        # )
        message.save()

    return render(request, 'candidate-information-messenger.html', context=context)


# TODO Аделина сделай нормальный css и html для этой страницы спасибо большое
@login_required
def hr_statistics(request):
    custom_request_user = CustomUser.objects.get(id=request.user.id)

    if custom_request_user.is_HR:
        target_hr = HR.objects.get(user_id=custom_request_user.id)
    elif custom_request_user.is_HRBP:
        target_hr = HRBP.objects.get(user_id=custom_request_user.id)
    else:
        return HttpResponseForbidden
    all_candidates_with_status, labels = [], []
    for i in range(len(CANDIDATE_STATUS_CHOICES)):
        if custom_request_user.is_HR:
            all_candidates_with_status.append(Candidate.objects.filter(vacancy__hR=target_hr, status=i).count())
        elif custom_request_user.is_HRBP:
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
        # 'user': request.user,
        'plot_data': plot_data
    }
    return render(request, 'hr-statistics.html', context=context)  #


@login_required
def vacancy_edit_add(request):
    custom_request_user = CustomUser.objects.get(id=request.user.id)
    vacancy = None
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
                              speciality_id=request.POST.get('speciality'),
                              testTaskDescription=request.POST.get('testTaskDescription'),
                              testTaskLink=request.POST.get('testTaskLink')
                              )
            if custom_request_user.is_HRBP:
                vacancy.hRBP = HRBP.objects.get(user_id=request.user.id)
                if request.POST.get('hR') != '':
                    vacancy.hR = HR.objects.get(id=request.POST.get('hR'))
            else:
                vacancy.hR = HR.objects.get(user_id=request.user.id)
                vacancy.hRBP = HRBP.objects.get(id=custom_request_user.hr.hRBP_id)
        else:
            vacancy = Vacancy.objects.get(id=request.POST.get('id'))
            vacancy.name = request.POST.get('name')
            vacancy.city_id = request.POST.get('city')
            if custom_request_user.is_HRBP and request.POST.get('hR') != '':
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
            vacancy.testTaskDescription = request.POST.get('testTaskDescription'),
            vacancy.testTaskLink = request.POST.get('testTaskLink')
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
    custom_request_user = CustomUser.objects.get(id=request.user.id)
    context = {
        # 'EMPLOYMENT_TYPE_CHOICES': dict(EMPLOYMENT_TYPE_CHOICES),
        # 'EDUCATION_CHOICES': dict(EDUCATION_CHOICES),
        # 'WORK_SCHEDULE_CHOICES': dict(WORK_SCHEDULE_CHOICES),
        # 'cities': City.objects.all().order_by('country_id'),
        # 'vacancy': Vacancy.objects.get(id=id),
        # 'specialities': Speciality.objects.all()
        "form": VacancyForm()
    }
    if custom_request_user.is_HRBP:
        context.update({'hrs': HRBP.objects.get(user_id=request.user.id).hr_set.all()})
    return render(request, 'vacancy-edit-or-add.html', context=context)


@login_required
def add_vacancy(request):
    custom_request_user = CustomUser.objects.get(id=request.user.id)
    context = {
        'EMPLOYMENT_TYPE_CHOICES': dict(EMPLOYMENT_TYPE_CHOICES),
        'EDUCATION_CHOICES': dict(EDUCATION_CHOICES),
        'WORK_SCHEDULE_CHOICES': dict(WORK_SCHEDULE_CHOICES),
        'cities': City.objects.all().order_by('country_id'),
        'specialities': Speciality.objects.all()
    }
    if custom_request_user.is_HRBP:
        context.update({'hrs': HRBP.objects.get(user_id=request.user.id).hr_set.all()})
    return render(request, 'vacancy-edit-or-add.html', context=context)


# @login_required
# class CreateHR(CreateView):
#     model = HR
#     fields = ["__all__"]
# def add_hr(request):
#     return render(request, 'hr-edit-or-add.html')


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
    custom_request_user = CustomUser.objects.get(id=request.user.id)

    if custom_request_user.is_HR:
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


@login_required
def vacancy_information(request, id):
    vacancy = Vacancy.objects.filter(id=id)[0]

    context = {
        'vacancy': vacancy,
        # 'candidates': Candidate.objects.filter(vacancy_id=vacancy.id)
    }
    return render(request, 'vacancy-information.html', context=context)


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
