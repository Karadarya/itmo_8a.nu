from django import template

register = template.Library()

@register.filter(name='route_comments')
def route_comments(comments, route):
    return comments.filter(route=route)[:3]
