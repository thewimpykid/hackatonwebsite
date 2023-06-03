from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Competition, Submission


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'size':'20', 'display':'block',}), required=True)
    grade = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "grade"]

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ["title", "description",  "min_age", "max_age"]

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["competition", "project_desc", "video"]