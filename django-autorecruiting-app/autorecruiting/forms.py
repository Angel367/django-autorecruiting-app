from .models import Vacancy
from django.views.generic import CreateView


# class CreateVacancy(CreateView):
#     model = Vacancy
#     fields = ["__all__"]
    # class AssignNewVacancyToCandidate(forms.Form):
    #     vacancies = forms.MultipleChoiceField(
    #         widget=forms.CheckboxSelectMultiple,
    #         choices=Vacancy.objects.filter(
    #
    #         ),
    #     )
    #  not archived
    #  not candidate`s vacancy