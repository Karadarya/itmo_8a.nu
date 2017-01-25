from django import template

register = template.Library()

@register.filter(name='route_comments')
def route_comments(comments, route):
    return comments.filter(route=route)[:3]


@register.filter(name='period_list')
def period_list(routes, period):
    return routes.filter(period=period)
