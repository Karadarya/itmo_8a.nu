 # -*- coding: UTF-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
#from model_utils import FieldTracker

class Athlete_Info(models.Model):
    class Meta:
        verbose_name='спортсмен'
        verbose_name_plural='спортсмены'
    athlete = models.ForeignKey(User, verbose_name='спортсмен')
    last_name = models.CharField(blank=True, max_length=200, verbose_name='фамилия')
    first_name = models.CharField(blank=True, max_length=200, verbose_name='имя')
    score = models.FloatField(verbose_name='баллы')
    position = models.PositiveIntegerField(verbose_name='место')
    picture = models.ImageField(upload_to='profile_picture/', null=True, blank=True,verbose_name='фото')
    def __unicode__(self):
        return self.athlete.username
    def __str__(self):
        return self.athlete.username


class Grade(models.Model):
    class Meta:
        verbose_name='категория'
        verbose_name_plural='категории'
        ordering = ['grade']
    grade = models.CharField(max_length=50, verbose_name='категория')
    cost = models.SmallIntegerField(verbose_name='стоимость')
    def __unicode__(self):
        return self.grade
    def __str__(self):
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
    def __str__(self):
        return self.remark


class Route(models.Model):
    class Meta:
        verbose_name='трасса'
        verbose_name_plural='трассы'
        ordering = ['-created']
    name = models.CharField(max_length=200, verbose_name='название')
    grade = models.ForeignKey(Grade, verbose_name='категория')
    description = models.TextField(blank=True, verbose_name='описание')
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name='автор')#models.ForeignKey(User, blank=True, null=True, verbose_name='постановщик')
    created = models.DateTimeField(default=timezone.now, verbose_name='поставлена')
    is_active = models.BooleanField(default=True, verbose_name='активна')
    def __unicode__(self) :
        return self.name
    def __str__(self) :
        return self.name


class Period(models.Model):
    started = models.DateField(default=timezone.now, verbose_name='начало')
    current = models.BooleanField(default=False, verbose_name='текущий')
    finished = models.DateField(null=True, blank=True, verbose_name='конец')

    def __str__(self):
        if self.finished:
            return "%s.%s.%s - %s.%s.%s" %(self.started.day, self.started.month, self.started.year, self.finished.day, self.finished.month, self.finished.year)
        else:
            return "%s.%s.%s - now" %(self.started.day, self.started.month, self.started.year)
    def __unicode__(self):
        if self.finished:
            return "%s.%s.%s - %s.%s.%s" %(self.started.day, self.started.month, self.started.year, self.finished.day, self.finished.month, self.finished.year)
        else:
            return "%s.%s.%s - now" %(self.started.day, self.started.month, self.started.year)

    class Meta:
        verbose_name='Период'
        verbose_name_plural='Период'
        ordering = ['-started']
        unique_together = ("started", "finished")


class Athlete_Route(models.Model):
    athlete = models.ForeignKey(User, verbose_name='спортсмен')
    route = models.ForeignKey(Route, verbose_name='трасса')
    remark = models.ForeignKey(Remark, verbose_name='примечание')
    date = models.DateTimeField(default=timezone.now, verbose_name='дата')
    comment = models.TextField(blank=True, verbose_name='комментарий')
    period = models.ForeignKey(Period, verbose_name='период')#, default=Period.objects.filter(current=True))
#    tracker=FieldTracker()
    def __unicode__(self):
        return "%s - %s" %(self.athlete.username, self.route.name)
    def __str__(self):
        return "%s - %s" %(self.athlete.username, self.route.name)
    class Meta:
        verbose_name='спортсмен_трасса'
        verbose_name_plural='спортсмены_трассы'
        #ordering = ['-date']
        unique_together = ("athlete", "route", "period")
