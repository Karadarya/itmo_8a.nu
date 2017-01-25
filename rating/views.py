 # -*- coding: UTF-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.contrib.auth import login, authenticate
from django.db import IntegrityError

from .models import Athlete_Info, Athlete_Route, Route, Period
from .forms import Athlete_Route_Form, RegisterForm, Route_Form, ProfileForm

def welcome(request):
    context = {}
    if not request.user.is_active:
        return render(request, 'welcome.html', context)
    else :
        return redirect('athlete_routes',
            username=request.user.username)

def rating(request):
    athletes = Athlete_Info.objects.filter(score__gt=0).order_by('position')
    context = {'athletes': athletes}
    return render(request, 'rating/rating.html', context)

def athlete_routes(request, username):
    athlete = get_object_or_404(Athlete_Info, athlete__username=username)
    routes = Athlete_Route.objects.filter(athlete__username=username).order_by('-remark__cost').order_by('-route__grade__cost')
    periods = Period.objects.all()
    context = {'routes': routes, 'athlete': athlete, 'periods': periods}
    return render(request, 'rating/athlete_routes.html', context)

@login_required
def add_route(request):
    if request.method == 'POST':
        form = Athlete_Route_Form(data=request.POST)
        try:
            if form.is_valid():
                route = form.save(commit=False)
                route.athlete = request.user
                if (Period.objects.exclude(current=True).filter(finished__gt=route.date)) :
                    route.period = Period.objects.exclude(current=True).filter(finished__gt=route.date).get(started__lt=route.date)
                else :
                    route.period = Period.objects.get(current=True)
                route.save()
                form.save_m2m()
                return redirect('athlete_routes',
                    username=request.user.username)
        except (IntegrityError):
            return render(request, 'rating/add_route.html', {
                'form': form,
                'error_message': "Вы уже добавили этот ТОР",
        })

    else:
        form = Athlete_Route_Form()
    context = {'form': form, 'create': True}
    return render(request, 'rating/add_route.html', context)

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            register = form.save(commit=False)
            register.save()
            form.save_m2m()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile_edit', username=username)
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'rating/register.html', context)

@login_required
def new_route(request):
    if request.method == 'POST':
        form = Route_Form(data=request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            if (request.user.last_name!="")|(request.user.first_name!=""):
                route.author = request.user.last_name+" "+request.user.first_name
            else:
                route.author = request.user.username
            route.save()
            form.save_m2m()
            return redirect('route_list')
    else:
        form = Route_Form()
    context = {'form': form, 'create': True}
    return render(request, 'rating/new_route.html', context)

def route_list(request):
    routes = Route.objects.all().order_by('grade')
    comments = Athlete_Route.objects.order_by('-date')
    context = {'routes': routes, 'comments': comments}
    return render(request, 'rating/route_list.html', context)

@login_required
def profile_edit(request, username):
    profile = get_object_or_404(Athlete_Info, athlete__username=username)
    if profile.athlete != request.user and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        form = ProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('athlete_profile', username=username)
    else:
        form = ProfileForm(instance=profile)
    context = {'form': form, 'create': False}
    return render(request, 'rating/profile_edit.html', context)

#doesn't work idk why
"""
@login_required
def route_edit(request, id) :
    route = get_object_or_404(Route, id=id)
    if route.author != request.user and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST' :
        form = Route_Form(instance=route, data=request.POST)
        old_grade = form.data['grade']
        if form.is_valid():
            new_grade = form.cleaned_data['grade']
            if old_grade != new_grade :
                raise PermissionDenied
            else:
                #if form.is_valid():
                form.save()
                return redirect('athlete_profile', username=User.username)
    else:
        form = Route_Form()
    context = {'form': form, 'create': False}
    return render(request, 'rating/route_edit.html', context)
"""

def athlete_profile(request, username):
    athlete = get_object_or_404(Athlete_Info, athlete__username=username)
    context = {'athlete': athlete}
    return render(request, 'rating/athlete_profile.html', context)

def route_info(request, id):
    route = get_object_or_404(Route, id=id)
    comments = Athlete_Route.objects.filter(route__id=id).order_by('-date')
    context = {'route': route, 'comments': comments}
    return render(request, 'rating/route_info.html', context)
