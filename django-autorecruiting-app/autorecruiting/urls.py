from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index),
    re_path(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('login/', views.login_view, name='login'),
    path('candidate-information/messenger/<int:id>', views.candidate_information_messenger, name='candidate-main'),
    path('candidate-information/main/<int:id>', views.candidate_information_main, name='candidate-messenger'),
    path('candidates/', views.candidates, name='candidates'),
    path('find-candidates/', views.find_candidates, name='find-candidates'),
    path('candidates-by-vacancy-id/<int:id>', views.candidates_by_vacancy_id, name='candidates-by-vacancy-id'),
    path('add-vacancy/', views.add_vacancy, name='add-vacancy'),
    path('edit-vacancy/<int:id>', views.edit_vacancy, name='edit-vacancy'),
    path('search-resumes/', views.search_resumes, name='search-resumes'),
    path('vacancy-edit-add/', views.vacancy_edit_add, name='add-edit-post-vacancy'),

    path('hr-edit-add/', views.hr_edit_add, name='add-edit-post-hr'),
    path('hr/add/', views.add_hr, name='add-hr'),
    path('hr/edit-by-id/<int:id>', views.edit_hr_by_id, name='edit-hr-by-id'),

    path('hr/all/', views.hr_all, name='hr-all'),

    path('hr/archive-vacancies/', views.hr_archive_vacancies, name='hr-archive-vacancies'),
    path('hr/vacancies/', views.hr_vacancies, name='hr-vacancies'),

    path('hr/<int:id>/own-vacancies/', views.hr_own_vacancies, name='hr-by-id-own-vacancies'),
    path('hr/statistics/', views.hr_statistics, name='hr-statistics'),
    path('hr/messenger/', views.hr_messenger, name='hr-messenger'),
    path('vacancy-information/<int:id>', views.vacancy_information, name='vacancy-information'),
    # path('hr/messenger/hrbp', views.hr_vacancies, name='hr-messenger-hrbp'),
    # path('hr/messenger/employer', views.hr_vacancies, name='hr-messenger-employer'),
    # path('hr/messenger/hrbp-to-hrs', views.hr_vacancies, name='hrs-messenger-hrbp'),

    #messenger
    # path('send_message/', views.send_message, name='send_message'),
    # path('get_messages/<int:user_id>/<int:recipient_id>/', views.get_messages, name='get_messages'),

    path('messages/', views.message_list, name='message_list'),
    # path('register/', views.register_page, name='register_page'),
    path('send_message/', views.send_message, name='send_message'),
    # path('create_user/', views.create_user, name='create_user'),
    path('get_user/<str:username>', views.get_user, name='get_user'),
    # path('user_messages/<str:username>/', views.get_user_messages, name='user_messages'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
