from django.urls import path
from .views import login_view, player_signup

urlpatterns = [
    path('', login_view, name='login'),
    path('player-signup/', player_signup, name='player_signup'),
]
