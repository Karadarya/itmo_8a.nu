 # -*- coding: UTF-8 -*-

from django import forms
from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Athlete_Route, Route, Athlete_Info

class Athlete_Route_Form(ModelForm):
    class Meta:
        model = Athlete_Route
        exclude = ('athlete',)

class Route_Form(ModelForm):
    class Meta:
        model = Route
        exclude = ('author', 'is_active')

class RegisterForm(UserCreationForm) :
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class ProfileForm(ModelForm):
    class Meta:
        model = Athlete_Info
        exclude = ('athlete', 'score', 'position')
