# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class RatingConfig(AppConfig):
    name = 'rating'
    verbose_name = 'Рейтинг'

    def ready(self):
        import rating.signals
