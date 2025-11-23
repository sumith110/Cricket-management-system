from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from cricket.models import Ball, Match, Team
from django.db import models


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

@login_required
def enter_ball(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    max_balls = match.overs * 6


    total_balls = Ball.objects.filter(
        match=match,
        innings=match.current_innings
    ).count()

    # Stop match when both innings done
    if total_balls >= max_balls:
            if match.current_innings == 1:
                # Switch to Team 2 innings
                match.current_innings = 2
                match.save()
                return redirect('enter_ball', match_id=match.id)
            else:
                # End match after 2nd innings
                match.is_completed = True
                match.save()
                return redirect('match_completed', match_id=match.id)
            
    next_over = (total_balls // 6) + 1
    next_ball = (total_balls % 6) + 1

    if request.method == "POST":
        runs = int(request.POST.get("runs", 0))
        is_wicket = request.POST.get("is_wicket") == "on"
        extra = request.POST.get("extra")

        count_ball = extra not in ['wide', 'no_ball']

        # Save Ball
        if count_ball:
            Ball.objects.create(
                match=match,
                innings=match.current_innings,
                over=next_over,
                ball_number=next_ball,
                runs=runs,
                is_wicket=is_wicket
            )

        # Update score
        if match.current_innings == 1:
            match.team1_score += runs
        else:
            match.team2_score += runs

        match.save()

        return redirect('enter_ball', match_id=match.id)

    # Live Scores
    total_runs = match.team1_score if match.current_innings == 1 else match.team2_score

    wickets = Ball.objects.filter(
        match=match, 
        innings=match.current_innings,
        is_wicket=True
    ).count()

    batting_team = match.team1 if match.current_innings == 1 else match.team2

    return render(request, 'umpire/enter_ball.html', {
        'match': match,
        'next_over': next_over,
        'next_ball': next_ball,
        'total_runs': total_runs,
        'wickets': wickets,
        'batting_team': batting_team
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
    matches = Match.objects.order_by('-id')  # Newest first


    return render(request, 'umpire/start_match.html', {
        'teams': teams,
        'matches': matches
    })

@login_required(login_url='umpire_login')
def match_completed(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    return render(request, 'umpire/match_completed.html', {'match': match})

