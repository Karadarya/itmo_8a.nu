from django.conf.urls import url
from rating import views

urlpatterns = [
    url(r'^athlete/(?P<username>[\S]+\w)/routes$', views.athlete_routes, name='athlete_routes'),
    url(r'^routes/add$', views.add_route, name='add_route'),
    url(r'^routes/new$', views.new_route, name='new_route'),
    url(r'^routes$', views.route_list, name='route_list'),
    url(r'^athlete/(?P<username>[\S]+\w)/profile/edit$', views.profile_edit, name='profile_edit'),
    url(r'^athlete/(?P<username>[\S]+\w)/profile$', views.athlete_profile, name='athlete_profile'),
    url(r'^register$', views.register_user, name='register_user'),
    url(r'^$', views.rating, name='rating'),
]
