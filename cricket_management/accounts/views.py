from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()

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

def player_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'accounts/player_signup.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/player_signup.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        return redirect('login')  # or change to your player login page

    return render(request, 'accounts/player_signup.html')