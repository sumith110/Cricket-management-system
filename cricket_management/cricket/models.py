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
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_matches')
    overs = models.IntegerField(default=20)

    # NEW FIELDS
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    current_innings = models.IntegerField(default=1)  # 1 or 2
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team1} vs {self.team2}"

class Ball(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    innings = models.IntegerField(default=1)  # NEW

    over = models.IntegerField()
    ball_number = models.IntegerField()

    runs = models.IntegerField(default=0)
    is_wicket = models.BooleanField(default=False)

