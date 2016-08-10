 # -*- coding: UTF-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate

from .models import Athlete_Info, Athlete_Route, Route
from .forms import Athlete_Route_Form, RegisterForm, Route_Form, ProfileForm


def rating(request):
    athletes = Athlete_Info.objects.order_by('position')
    context = {'athletes': athletes}
    return render(request, 'rating/rating.html', context)

def athlete_routes(request, username):
    #user = get_object_or_404(User, username=username)
    athlete = get_object_or_404(Athlete_Info, athlete__username=username)
    routes = Athlete_Route.objects.filter(athlete__username=username)
    context = {'routes': routes, 'athlete': athlete}
    return render(request, 'rating/athlete_routes.html', context)

@login_required
def add_route(request):
    if request.method == 'POST':
        form = Athlete_Route_Form(data=request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            route.athlete = request.user
            route.save()
            form.save_m2m()
            return redirect('athlete_routes',
                username=request.user.username)
    else:
        form = Athlete_Route_Form()
    context = {'form': form, 'create': True}
    return render(request, 'rating/add_route.html', context)

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)     # create form object
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
            route.author = request.user
            route.save()
            form.save_m2m()
            return redirect('route_list')
    else:
        form = Route_Form()
    context = {'form': form, 'create': True}
    return render(request, 'rating/new_route.html', context)

def route_list(request):
    routes = Route.objects.all()
    comments = Athlete_Route.objects.order_by('-date')
    #routes = tmp_routes.order_by('-date')
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

def athlete_profile(request, username):
    athlete = get_object_or_404(Athlete_Info, athlete__username=username)
    context = {'athlete': athlete}
    return render(request, 'rating/athlete_profile.html', context)
