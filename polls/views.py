from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import PollAddForm, PollEditForm, PollChoiceAddForm
from .models import *

def polls_list(request):
    polls = Poll.objects.all()

    paginator = Paginator(polls, 2)
    page = request.GET.get('page')
    paginated_polls = paginator.get_page(page)

    return render(request, 'polls/polls_list.html', {'polls': paginated_polls})

@login_required()
def user_polls_list(request):
    polls = Poll.objects.filter(owner=request.user)
    paginator = Paginator(polls, 2)
    page = request.GET.get('page')
    paginated_polls = paginator.get_page(page)

    return render(request, 'polls/polls_list.html', {'polls': paginated_polls})

@login_required()
def poll_add(request):
    if request.user.has_perm('polls.add_poll'):
        if request.method == 'POST':
            form = PollAddForm(request.POST)
            if form.is_valid():
                poll = form.save(commit=False)
                poll.owner = request.user
                poll.save()
                PollChoices(poll=poll, choice_text=form.cleaned_data['choice1']).save()
                PollChoices(poll=poll, choice_text=form.cleaned_data['choice2']).save()

                messages.success(request, 'Poll added successfully', extra_tags='alert alert-success alert-dismissible fade show')
                return redirect('polls:list_by_user')

        else:
            form = PollAddForm()
        return render(request, 'polls/add_poll.html', {'form': form})

    else:
        messages.error(request, "Sorry but you don't have permission to do that!", extra_tags='alert alert-danger alert-dismissible fade show')
        return redirect('polls:list')



def poll_edit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        messages.error(request, 'Your not the owner of this poll.', extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect('polls:list')

    if request.method == 'POST':
        form = PollEditForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            messages.success(request, 'Poll updated successfully.', extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:list_by_user')
    else:
        form = PollEditForm(instance=poll)
    return render(request, 'polls/poll_edit.html', {'poll': poll, 'form': form})
