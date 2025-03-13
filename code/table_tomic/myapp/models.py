from django.db import models

# Create your models here.
# class TodoItem(models.Model):
#     title = models.CharField(max_length=200)
#     completed = models.BooleanField(max_length=200)


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,unique=True)
    rep = models.CharField(max_length=100)
    match_win = models.IntegerField()
    match_total = models.IntegerField()
    tomic_level = models.FloatField()

class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    timestamp = models.DateField(auto_now=True)
    team1_goalkeeper = models.ForeignKey(Player, related_name='g1',on_delete=models.SET_NULL, null=True)
    team1_attacker = models.ForeignKey(Player,related_name='g2' ,on_delete=models.SET_NULL, null=True)
    team2_goalkeeper = models.ForeignKey(Player, related_name='g3',on_delete=models.SET_NULL, null=True)
    team2_attacker = models.ForeignKey(Player, related_name='g4',on_delete=models.SET_NULL, null=True)
    team1_goals = models.IntegerField()
    team2_goals = models.IntegerField()

