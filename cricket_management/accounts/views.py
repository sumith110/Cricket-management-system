from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print(user.role)
            if user.role == 'umpire':
                return redirect('/umpire/')
            elif user.role == 'player':
                return redirect('/player/')
            else:
                return redirect('/admin/')
        else:
            context['error'] = "Invalid username or password"

    return render(request, 'accounts/login.html', context)
