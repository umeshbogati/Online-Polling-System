from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Poll, Choice, Vote


# Create your views here.
@login_required
def poll_list(request):
    polls = Poll.objects.all()
    return render(request, 'polls/poll_list.html', {'polls': polls})         

@login_required
def poll_detail(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    choices = Choice.objects.filter(poll=poll)
    return render(request, 'poll_detail.html', {'poll': poll, 'choices': choices})  

@login_required
def vote(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    if Vote.objects.filter(user=request.user, poll=poll).exits():
        return redirect('result', poll_id=poll.id)
    choice_id = request.POST.get('choice')
    choice = choice.objects.get(id=choice_id)
    choice.votes += 1 
    choice.save()
    Vote.objects.create(user=request.user, poll=poll)
    return redirect('result', poll_id=poll.id)

@login_required
def result(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    choices = Choice.objects.filter(poll=poll)
    return render(request, 'result.html', {'poll': poll, 'choices': choices})
                                    