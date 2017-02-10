from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.db.models import F, Max, Sum
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from rating.models import Athlete_Info, Athlete_Route, Route, Period

def check_best_results(ath, new_top):
    num_of_res = 6
    best_results = Athlete_Route.objects.order_by('route__grade__cost')[:num_of_res]
    if new_top in best_results:
        """ath.update()"""
        pass

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

#def count_points(instance):


@receiver(post_save, sender=User)
def new_athlete_signal(instance, **kwargs):
    if not Athlete_Info.objects.filter(athlete=instance).exists():
        p=Athlete_Info.objects.aggregate(Max('position'))
        Athlete_Info.objects.create(athlete=instance, score=0, position=p['position__max']+1)

def recount(instance, case):
    num_of_res=6
    best = Athlete_Route.objects.filter(athlete=instance.athlete).filter(period=Period.objects.get(current=True)).order_by('-remark__cost').order_by('-route__grade__cost')[:num_of_res]
    if case == "delete" :
        if (instance in best):
            new_best=Athlete_Route.objects.filter(athlete=instance.athlete).filter(period=Period.objects.get(current=True)).exclude(route=instance.route).order_by('-remark__cost').order_by('-route__grade__cost')[:num_of_res]
            sum_points=new_best.aggregate(best_points=Sum(F('route__grade__cost')+F('remark__cost')))
            #best_points=sum_points['best_points']
            Athlete_Info.objects.filter(athlete=instance.athlete).update(score=sum_points['best_points'])
            rating_update(instance.athlete, "down")

    elif case == "add" :
        if (instance in best):
            sum_points=best.aggregate(best_points=Sum(F('route__grade__cost')+F('remark__cost')))
            #best_points=sum_points['best_points']
            Athlete_Info.objects.filter(athlete=instance.athlete).update(score=sum_points['best_points'])
            rating_update(instance.athlete, "up")

    elif case == "recount" :
            sum_points=best.aggregate(best_points=Sum(F('route__grade__cost')+F('remark__cost')))
            pre_score = Athlete_Info.objects.values_list('score', flat=True).get(athlete=instance.athlete)
            if pre_score > sum_points :
                way = "down"
            elif pre_score < sum_points :
                way = "up"
            Athlete_Info.objects.filter(athlete=instance.athlete).update(score=sum_points['best_points'])
            rating_update(instance.athlete, way)


@receiver(pre_delete, sender=Athlete_Route)
def del_old_points(instance, **kwargs):
    recount(instance, "delete")
    #shameless copy-paste

@receiver(post_save, sender=Athlete_Route)
def add_new_points(instance, created, **kwargs):
    if ( created == True ):
        recount(instance, "add")

@receiver(post_save, sender=Athlete_Route)
def change_points(instance, created, **kwargs):
    if ( created == False ) :
        recount(instance, "recount")


@receiver(post_save, sender=Route)
def route_changed(instance, created, **kwargs):
    if ( created == False ):
        ath_routes=Athlete_Route.objects.filter(route=instance)
        for ath_route in ath_routes:
            change_points(ath_route, False)


@receiver(post_save, sender=Athlete_Info)
def add_user_name(instance, **kwargs):
    User.objects.filter(username=instance.athlete.username).update(first_name=instance.first_name, last_name=instance.last_name)

@receiver(post_save, sender=Period)
def new_period(instance, **kwargs):
    per = Period.objects.filter(current=True)
    per.update(finished=timezone.now())
    per.update(current=False)
    Period.objects.filter(id=instance.id).update(current=True)
    Athlete_Info.objects.all().update(score=0)
