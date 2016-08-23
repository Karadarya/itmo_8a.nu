from django.db.models.signals import post_save, post_delete, pre_save
from django.db.models import F, Max
from django.dispatch import receiver
from django.contrib.auth.models import User
from rating.models import Athlete_Info, Athlete_Route


def rating_update(ath, way):
    init_pos = Athlete_Info.objects.values_list('position', flat=True).get(athlete=ath)
    self_score = Athlete_Info.objects.values_list('score', flat=True).get(athlete=ath)
    if (way=="up")&(init_pos!=1):
        """check if there were equals"""
        if Athlete_Info.objects.filter(position=init_pos).count()>1 :
            aths_down = Athlete_Info.objects.filter(position__gte=init_pos).exclude(athlete=ath)
            aths_down.update(position=F('position')+1)
        upper_score = Athlete_Info.objects.values('score').filter(position=init_pos-1)[0]['score']
        if (self_score<upper_score): return
        while(self_score>upper_score)|(self_score==upper_score):
            if (self_score>upper_score):
                ath_up = Athlete_Info.objects.filter(athlete=ath)
                aths_down = Athlete_Info.objects.filter(position=init_pos-1)
                aths_down.update(position=F('position')+1)
                ath_up.update(position=F('position')-1)
                init_pos-=1
                if init_pos==1 : break
                upper_score = Athlete_Info.objects.values('score').filter(position=init_pos-1)[0]['score']
            if (self_score==upper_score):
                aths_up = Athlete_Info.objects.filter(position__gte=init_pos)
                aths_up.update(position=F('position')-1)
                return

    #seems to work.  testing will show
    if (way=="down")& Athlete_Info.objects.filter(position=init_pos+1).exists():
        #it works, but I dunno why -_-"
        if Athlete_Info.objects.filter(position=init_pos).count()>1 :
            dic=Athlete_Info.objects.aggregate(Max('position'))
            self_pos=dic['position__max']
            while self_pos>=init_pos:
                aths_down=Athlete_Info.objects.filter(position=self_pos)
                aths_down.update(position=F('position')+1)
                self_pos-=1
        if Athlete_Info.objects.filter(position=init_pos+1).exists():
            lower_score = Athlete_Info.objects.values('score').filter(position=init_pos+1)[0]['score']
        else: return
        while(self_score<lower_score)|(self_score==lower_score):
            if (self_score<lower_score):
                ath_down = Athlete_Info.objects.filter(athlete=ath)
                aths_up = Athlete_Info.objects.filter(position=init_pos+1)
                aths_up.update(position=F('position')-1)
                ath_down.update(position=F('position')+1)
                init_pos+=1
                if Athlete_Info.objects.filter(position=init_pos+1).exists():
                    lower_score = Athlete_Info.objects.values('score').filter(position=init_pos+1)[0]['score']
                else : break
            if (self_score==lower_score):
                aths_up = Athlete_Info.objects.filter(position__gt=init_pos)
                aths_up.update(position=F('position')-1)
                return

@receiver(post_save, sender=User)
def new_athlete_signal(instance, **kwargs):
    if not Athlete_Info.objects.filter(athlete=instance).exists():
        Athlete_Info.objects.create(athlete=instance, score=0, position=Athlete_Info.objects.count()+1)

@receiver(post_delete, sender=Athlete_Route)
def del_old_points(instance, **kwargs):
    ath = Athlete_Info.objects.filter(athlete=instance.athlete)
    ath.update(score=F('score')-(instance.grade.cost+instance.remark.cost))
    rating_update(instance.athlete, "down")


@receiver(post_save, sender=Athlete_Route)
def add_new_points(instance, **kwargs):
    ath = Athlete_Info.objects.filter(athlete=instance.athlete)
    ath.update(score=F('score')+(instance.grade.cost+instance.remark.cost))
    rating_update(instance.athlete, "up")

@receiver(post_save, sender=Athlete_Info)
def add_user_name(instance, **kwargs):
    User.objects.filter(username=instance.athlete.username).update(first_name=instance.first_name, last_name=instance.last_name)
