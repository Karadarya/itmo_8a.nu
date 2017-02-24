from django import template
from rating.models import Athlete_Route, Period
from django.db.models import Sum, F

register = template.Library()

@register.filter(name='route_comments')
def route_comments(comments, route):
    return comments.filter(route=route)[:3]


@register.filter(name='period_list')
def period_list(routes, period):
    return routes.filter(period=period)

@register.filter(name='rated')
def rated(route):
    #might need optimization
    best = Athlete_Route.objects.filter(athlete=route.athlete).filter(period=Period.objects.get(current=True)).annotate(sum=Sum(F('route__grade__cost')+F('remark__cost'))).order_by('-sum')[:6]
    if  ( route in best ):
        return True
    else:
        return False
