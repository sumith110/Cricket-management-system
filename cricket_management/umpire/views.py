from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from cricket.models import Match, Team

def umpire_home(request):
    # If not logged in → go to login
    if not request.user.is_authenticated:
        return redirect('umpire_login')

    # If logged in but NOT umpire → block
    if request.user.role != 'umpire':
        return HttpResponseForbidden("You are not an umpire")

    return redirect('umpire_dashboard')

@login_required(login_url='umpire_login')
def umpire_dashboard(request):
    if request.user.role != 'umpire':
        return HttpResponseForbidden("Access denied")

    return render(request, 'umpire/dashboard.html')


from cricket.models import Match, Ball

@login_required(login_url='umpire_login')
def enter_ball(request, match_id):
    if request.user.role != 'umpire':
        return HttpResponseForbidden("Access denied")

    match = Match.objects.get(id=match_id)

    # Count balls already bowled for this match
    balls = Ball.objects.filter(match=match).order_by('id')
    total_balls = balls.count()

    # Calculate next over & ball number
    next_over = total_balls // 6 + 1
    next_ball = total_balls % 6 + 1

    # Prevent scoring beyond allowed overs
    if next_over > match.overs:
        return HttpResponseForbidden("Match completed — all overs finished")

    return render(request, 'umpire/enter_ball.html', {
        'match': match,
        'match_id': match_id,
        'next_over': next_over,
        'next_ball': next_ball,
        'total_balls': total_balls,
    })




    
@login_required(login_url='umpire_login')
def start_match(request):
    if request.user.role != 'umpire':
        return HttpResponseForbidden("Access denied")

    if request.method == 'POST':
        team1_id = request.POST.get('team1')
        team2_id = request.POST.get('team2')
        overs = request.POST.get('overs')  # <-- added

        if team1_id and team2_id and team1_id != team2_id and overs:
            Match.objects.create(
                team1_id=team1_id,
                team2_id=team2_id,
                overs=overs
            )
            return redirect('start_match')

    teams = Team.objects.all()
    matches = Match.objects.all()

    return render(request, 'umpire/start_match.html', {
        'teams': teams,
        'matches': matches
    })
