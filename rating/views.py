 # -*- coding: UTF-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.contrib.auth import login, authenticate
from django.db import IntegrityError

from .models import Athlete_Info, Athlete_Route, Route, Period
from .forms import Athlete_Route_Form, RegisterForm, Route_Form, ProfileForm, Delete_Athlete_Route_Form

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
    routes = Athlete_Route.objects.filter(athlete__username=username).order_by('-route__grade__cost','-remark__cost')
    periods = Period.objects.all()
    requestor = request.user
    context = {'routes': routes, 'athlete': athlete, 'periods': periods, 'requestor':requestor}
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

@login_required
def delete_route(request, id):
    ath_route = get_object_or_404( Athlete_Route, id=id)
    if ath_route.athlete != request.user and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        form = Delete_Athlete_Route_Form(data=request.POST, instance=ath_route)
        if form.is_valid():
            ath_route.delete()
            return redirect('athlete_routes',
                username=request.user.username)
    else:
        form = Delete_Athlete_Route_Form(instance=ath_route)
    context = {'form': form, 'create': False, 'ath_route': ath_route}
    return render(request, 'rating/delete_route.html', context)


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
    routes = Route.objects.all().filter(is_active=True).order_by('grade')
    comments = Athlete_Route.objects.filter(route__is_active=True).order_by('-date')
    if (request.user.last_name!="")|(request.user.first_name!=""):
        requestor = request.user.last_name+" "+request.user.first_name
    else:
        requestor = request.user.username
    context = {'routes': routes, 'comments': comments, 'requestor': requestor}
    return render(request, 'rating/route_list.html', context)

@login_required
def profile_edit(request, username):
    profile = get_object_or_404(Athlete_Info, athlete__username=username)
    if profile.athlete != request.user and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            m = Athlete_Info.objects.get(athlete__username=username)
            m.picture = form.cleaned_data['picture']
            m.save()
            return redirect('athlete_profile', username=username)
    else:
        form = ProfileForm(instance=profile)
    context = {'form': form, 'create': False}
    return render(request, 'rating/profile_edit.html', context)

#to be done. Maybe. Someday
"""
@login_required
def athlete_route_edit(request, route_id):
    ath_route = get_object_or_404(Athlete_Route, athlete=request.user, route=route_id)
    if profile.athlete != request.user and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        form = Athlete_Route_Form(instance=ath_route, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('athlete_routes', username=username)
    else:
        form = Athlete_Route_Form(instance=ath_route)
    context = {'form': form, 'create': False}
    return render(request, 'rating/athlete_route_edit.html', context)"""

#doesn't work idk why

@login_required
#saves everything to route with id=10. WTF???
def route_edit(request, id) :
    route = get_object_or_404(Route, pk=id)
    #permission check
    """if (request.user.last_name!="")|(request.user.first_name!=""):
        author = request.user.last_name+" "+request.user.first_name
    else:
        author = request.user.username
    if route.author != author :
        raise PermissionDenied"""
    if request.method == 'POST' :
        #route = get_object_or_404(Route, pk=id)
        form = Route_Form( instance = route, data = request.POST)
        #old_grade = form.data['grade']
        if form.is_valid():
            form.save()
            return redirect('route_list')
    else:
        route = get_object_or_404(Route, id=id)
        form = Route_Form(instance=route)
    context = {'form': form, 'create': False, 'route': route}
    return render(request, 'rating/route_edit.html', context)


def athlete_profile(request, username):
    athlete = get_object_or_404(Athlete_Info, athlete__username=username)
    context = {'athlete': athlete}
    return render(request, 'rating/athlete_profile.html', context)

def route_info(request, id):
    route = get_object_or_404(Route, id=id)
    comments = Athlete_Route.objects.filter(route__id=id).order_by('-date')
    context = {'route': route, 'comments': comments}
    return render(request, 'rating/route_info.html', context)
