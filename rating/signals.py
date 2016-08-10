from django.db.models.signals import post_save, post_delete, pre_save
from django.db.models import F
from django.dispatch import receiver
from django.contrib.auth.models import User
from rating.models import Athlete_Info, Athlete_Route


def rating_update(ath, way):
    """equal score to be done. nope =_= """
    init_pos = Athlete_Info.objects.values_list('position', flat=True).get(athlete=ath)
    self_score = Athlete_Info.objects.values_list('score', flat=True).get(position=init_pos)
    if (way=="up")&(init_pos!=1):
        upper_score = Athlete_Info.objects.values_list('score', flat=True).get(position=init_pos-1)
        if (self_score<=upper_score): return
        if (self_score>upper_score):
            while(self_score>upper_score):
                ath_up = Athlete_Info.objects.filter(athlete=ath)
                ath_down = Athlete_Info.objects.filter(position=init_pos-1)
                ath_up.update(position=F('position')-1)
                ath_down.update(position=F('position')+1)
                init_pos-=1
                if init_pos==1 : break
                upper_score = Athlete_Info.objects.values_list('score', flat=True).get(position=init_pos-1)
            #if [not (self_score==lower_score)] clause needed if equal_score_variant is added
            Athlete_Info.objects.filter(athlete=ath).update(position=F('position')-1)

    if (way=="down")&(init_pos!=Athlete_Info.objects.count()):
        lower_score = Athlete_Info.objects.values_list('score', flat=True).get(position=init_pos+1)
        if (self_score>=lower_score): return
        if (self_score<lower_score):
            while(self_score<lower_score):
                ath_down = Athlete_Info.objects.filter(athlete=ath)
                ath_up = Athlete_Info.objects.filter(position=init_pos+1)
                ath_down.update(position=F('position')+1)
                ath_up.update(position=F('position')-1)
                init_pos+=1
                if init_pos==Athlete_Info.objects.count() : break
                lower_score = Athlete_Info.objects.values_list('score', flat=True).get(position=init_pos+1)
            Athlete_Info.objects.filter(athlete=ath).update(position=F('position')+1)

@receiver(post_save, sender=User)
def new_athlete_signal(instance, **kwargs):
    if not Athlete_Info.objects.filter(athlete=instance).exists():
        Athlete_Info.objects.create(athlete=instance, score=0, position=Athlete_Info.objects.count()+1)

@receiver(post_delete, sender=Athlete_Route)
def del_old_points(instance, **kwargs):
    #if Athlete_Route.objects.filter(athlete=instance.athlete).filter(route=instance.route):
    ath = Athlete_Info.objects.filter(athlete=instance.athlete)
    ath.update(score=F('score')-(instance.grade.cost+instance.remark.cost))
    rating_update(instance.athlete, "down")
        #ath.score-=instance.remark.cost

@receiver(post_save, sender=Athlete_Route)
def add_new_points(instance, **kwargs):
    #if not Athlete_Route.objects.filter(athlete=instance.athlete).filter(route=instance.route).exists():
    ath = Athlete_Info.objects.filter(athlete=instance.athlete)
    ath.update(score=F('score')+(instance.grade.cost+instance.remark.cost))
    rating_update(instance.athlete, "up")

@receiver(post_save, sender=Athlete_Info)
def add_user_name(instance, **kwargs):
    User.objects.filter(username=instance.athlete.username).update(first_name=instance.first_name, last_name=instance.last_name)
