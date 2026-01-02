from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Poll, Choice, Vote
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

# --- Login/Logout ---
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('poll_list')
        else:
            return render(request, 'polls/login.html', {'error': 'Invalid username or password'})
    return render(request, 'polls/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')

# --- Poll list ---
@login_required
def poll_list(request):
    polls = Poll.objects.all()
    return render(request, 'polls/poll_list.html', {'polls': polls})

# --- Poll detail with choices ---
@login_required
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    choices = Choice.objects.filter(poll=poll)
    return render(request, 'polls/poll_detail.html', {'poll': poll, 'choices': choices})

# --- Vote ---
@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if poll.end_date < timezone.now():
        return render(request, 'closed.html')
    # Check if user has already voted
    if Vote.objects.filter(user=request.user, poll=poll).exists():
        return redirect('result', poll_id=poll.id)

    if request.method == 'POST':
        choice_ids = request.POST.getlist('choices')  # Multiple choice
        for cid in choice_ids:
            choice = Choice.objects.get(id=cid)
            choice.votes += 1
            choice.save()

        Vote.objects.create(user=request.user, poll=poll)
        return redirect('result', poll_id=poll.id)

    return redirect('poll_detail', poll_id=poll.id)

# --- Results ---
@login_required
def result(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    choices = Choice.objects.filter(poll=poll)
    return render(request, 'polls/result.html', {'poll': poll, 'choices': choices})

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created sucessfully')
            return redirect('login')
    return render(request, 'polls/register.html')