 # -*- coding: UTF-8 -*-

from django.contrib import admin

from .models import Athlete_Info, Route, Grade, Remark, Athlete_Route, Season

class Athlete_Info_Admin(admin.ModelAdmin):
    list_display = ('position', 'athlete', 'first_name', 'last_name', 'score')
    list_order_by = ('position',)
    search_fields = ['athlete']


class Route_Admin(admin.ModelAdmin):
    list_display = ('name', 'description', 'author', 'created', 'is_active')
    list_editable = ('is_active',)
    list_order_by = ('-created',)
    search_fields = ['name', 'description']

class Athlete_Route_Admin(admin.ModelAdmin):
    list_display = ('athlete', 'route', 'grade', 'remark', 'date')
    list_order_by = ('-date',)
    search_fields = ['athlete', 'route']
    list_filter = ('route', 'athlete',)
    readonly_fields = ('athlete', 'route', 'grade', 'remark', 'date', 'comment')

class Season_Admin(admin.ModelAdmin):
    list_display = ('started', 'finished', 'current')
    list_order_by = ('-started',)

admin.site.register(Athlete_Info, Athlete_Info_Admin)
admin.site.register(Route, Route_Admin)
admin.site.register(Grade)
admin.site.register(Remark)
admin.site.register(Athlete_Route, Athlete_Route_Admin)
admin.site.register(Season, Season_Admin)
