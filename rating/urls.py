from django.conf.urls import url
#from . import views

urlpatterns = [
    url(r'^athlete/(?P<username>[\S]+\w)/routes$', 'rating.views.athlete_routes', name='athlete_routes'),
    url(r'^routes/add$', 'rating.views.add_route', name='add_route'),
    url(r'^routes/new$', 'rating.views.new_route', name='new_route'),
    url(r'^routes$', 'rating.views.route_list', name='route_list'),
    url(r'^athlete/(?P<username>[\S]+\w)/profile/edit$', 'rating.views.profile_edit', name='profile_edit'),
    url(r'^athlete/(?P<username>[\S]+\w)/profile$', 'rating.views.athlete_profile', name='athlete_profile'),

    #url(r'^/$', views.post_create, name='post_create'),
    #url(r'^rating/$', 'rating.views.rating', name='rating'),
    url(r'^register$', 'rating.views.register_user', name='register_user'),
    url(r'^$', 'rating.views.rating', name='rating'),
]
