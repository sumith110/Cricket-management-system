from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('umpire', 'Umpire'),
        ('player', 'Player'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='player'   # ✅ important
    )
