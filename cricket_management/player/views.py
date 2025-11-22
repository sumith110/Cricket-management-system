from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

@login_required
def dashboard(request):
    if request.user.role != 'player':
        return HttpResponseForbidden("Not allowed")

    return render(request, 'player/dashboard.html')

