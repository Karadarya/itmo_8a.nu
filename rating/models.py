 # -*- coding: UTF-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Athlete_Info(models.Model):
    class Meta:
        verbose_name='спортсмен'
        verbose_name_plural='спортсмены'
    athlete = models.ForeignKey(User, verbose_name='спортсмен')
    last_name = models.CharField(blank=True, max_length=200, verbose_name='фамилия')
    first_name = models.CharField(blank=True, max_length=200, verbose_name='имя')
    score = models.FloatField(verbose_name='баллы')
    position = models.PositiveIntegerField(verbose_name='место')
    def __unicode__(self):
        return self.athlete.username



class Route(models.Model):
    class Meta:
        verbose_name='трасса'
        verbose_name_plural='трассы'
        ordering = ['-created']
    name = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(blank=True, verbose_name='описание')
    author = models.ForeignKey(User, blank=True, verbose_name='постановщик')
    created = models.DateTimeField(default=timezone.now, verbose_name='поставлена')
    is_active = models.BooleanField(default=True, verbose_name='активна')
    def __unicode__(self) :
        return self.name
    """def avg_grade(self):
        grade=Athlete_Route.objects.filter(route.name=route).aggregate(average_grade=AVG('grade'))
        to be continued"""

class Grade(models.Model):
    class Meta:
        verbose_name='категория'
        verbose_name_plural='категория'
        ordering = ['grade']
    grade = models.CharField(max_length=50, verbose_name='категория')
    cost = models.SmallIntegerField(verbose_name='стоимость')
    def __unicode__(self):
        return self.grade


class Remark(models.Model):
    class Meta:
        verbose_name='примечание'
        verbose_name_plural='примечания'
        ordering = ['remark']
    remark = models.CharField(max_length=50, verbose_name='примечание')
    cost = models.SmallIntegerField(verbose_name='стоимость')
    def __unicode__(self):
        return self.remark

class Athlete_Route(models.Model):
    athlete = models.ForeignKey(User, verbose_name='спортсмен')
    route = models.ForeignKey(Route, verbose_name='трасса')
    grade = models.ForeignKey(Grade, verbose_name='категория')
    remark = models.ForeignKey(Remark, verbose_name='примечание')
    date = models.DateTimeField(default=timezone.now, verbose_name='дата')
    comment = models.TextField(blank=True, verbose_name='комментарий')
    def __unicode__(self):
        return "%s - %s" %(self.athlete.username, self.route.name)
    class Meta:
        verbose_name='спортсмен_трасса'
        verbose_name_plural='спортсмены_трассы'
        ordering = ['-date']
        unique_together = ("athlete", "route")


class Season(models.Model):
    started = models.DateField(default=timezone.now, verbose_name='начало')
    current = models.BooleanField(default=True, verbose_name='текущий')
    finished = models.DateField(null=True, blank=True, verbose_name='конец')
    def __unicode__(self):
        if self.finished:
            return "%s %s - %s %s" %(self.started.month, self.started.year, self.finished.month, self.finished.year)
        else:
            return "%s %s - now" %(self.started.month, self.started.year)
    class Meta:
        verbose_name='сезон'
        verbose_name_plural='сезоны'
        ordering = ['-started']
        unique_together = ("started", "finished")
# Create your models here.
