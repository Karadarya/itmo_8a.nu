"""itmo_climbing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy
from rating import views, models
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class RouteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Route
        #fields = '__all__' #('id', 'name', 'grade')
        exclude = ('grade',)

# ViewSets define the view behavior.
class RouteViewSet(viewsets.ModelViewSet):
    queryset = models.Route.objects.all()
    serializer_class = RouteSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'routes', RouteViewSet)
#urlpatterns = router.urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^api-get-routes/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^rating/', include('rating.urls')),
    url(r'^login/$', login, {'template_name': 'login.html'},
        name='itmo_climbing_login'),
    url(r'^logout/$', logout,
        {'next_page': reverse_lazy('rating')}, name='itmo_climbing_logout'),
    url(r'^$', views.welcome, name='welcome'),
]
