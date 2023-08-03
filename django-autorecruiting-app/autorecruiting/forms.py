from django import forms
from .models import City, Speciality, EDUCATION_CHOICES, WORK_SCHEDULE_CHOICES, EMPLOYMENT_TYPE_CHOICES


class VacancyForm(forms.Form):
    name = forms.CharField(strip=True)
    vacancyDescription = forms.CharField(widget=forms.Textarea)
    testTaskDescription = forms.CharField(widget=forms.Textarea)
    testTaskLink = forms.CharField(strip=True)
    chosenLetter = forms.CharField(widget=forms.Textarea)
    testTaskLetter = forms.CharField(widget=forms.Textarea)
    educationLevel = forms.ChoiceField(choices=EDUCATION_CHOICES)
    employmentType = forms.ChoiceField(choices=EMPLOYMENT_TYPE_CHOICES)
    workSchedule = forms.ChoiceField(choices=WORK_SCHEDULE_CHOICES)
    workExperienceFrom = forms.IntegerField(step_size=1, min_value=12000)
    workExperienceTo = forms.IntegerField(step_size=1, min_value=12000)
    suggestedSalaryFrom = forms.IntegerField(step_size=1000, min_value=10000)
    suggestedSalaryTo = forms.IntegerField(step_size=1000, min_value=10000)
    city = forms.ChoiceField(choices=[(o.id, str(o)) for o in City.objects.all()])
    speciality = forms.ChoiceField(choices=[(o.id, str(o)) for o in Speciality.objects.all()])




