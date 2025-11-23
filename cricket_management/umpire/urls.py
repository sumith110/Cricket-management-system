from django.urls import path
from . import views

urlpatterns = [
    path('', views.umpire_home, name='umpire_home'),
    path('dashboard/', views.umpire_dashboard, name='umpire_dashboard'),
    path('start-match/', views.start_match, name='start_match'),
    path('score/<int:match_id>/', views.enter_ball, name='enter_ball'),
    path('match/<int:match_id>/completed/', views.match_completed, name='match_completed'),
]
