from django.db import models
from accounts.models import User

class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2')
    overs = models.IntegerField(default=20)
    is_active = models.BooleanField(default=False)


class Ball(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    over = models.IntegerField()
    ball_number = models.IntegerField()
    runs = models.IntegerField()
    is_wicket = models.BooleanField(default=False)
