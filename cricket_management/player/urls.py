from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.player_profile, name='player_profile'),
    path('matches/', views.player_matches, name='player_matches'),
]
