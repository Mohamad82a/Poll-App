from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import PollAddForm, PollEditForm, PollChoiceAddForm
from .models import *
from django.db.models import Q
def polls_list(request):
    polls = Poll.objects.all()
    search_term = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        polls = Poll.objects.filter(
            Q(title__icontains=search_term)
        )
        # if polls == '':
        #     messages.error(request, 'No results found', extra_tags='alert alert-warning alert-dismissible fade show')
        #

    paginator = Paginator(polls, 3)
    page = request.GET.get('page')
    paginated_polls = paginator.get_page(page)

    return render(request, 'polls/polls_list.html', {'polls': paginated_polls, 'search_term': search_term})

@login_required()
def user_polls_list(request):
    polls = Poll.objects.filter(owner=request.user)
    paginator = Paginator(polls, 3)
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


@login_required()
def poll_delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    poll_title = poll.title
    poll.delete()
    messages.success(request, f"Your poll ({poll_title[:15]}) has been deleted successfully.", extra_tags='alert alert-success alert-dismissible fade show')
    return redirect('polls:list_by_user')


@login_required()
def choice_add(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'POST':
        form = PollChoiceAddForm(request.POST)
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(request, f'New choice added to your poll ({poll.title[:15]})', extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:detail_poll') #Should go to poll detail

    else:
        form = PollChoiceAddForm

    return render(request, 'polls/add_choice.html', {'poll': poll, 'form': form})

@login_required()
def choice_edit(request, choice_id):
    choice = get_object_or_404(PollChoices, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.method == 'POST':
        form = PollChoiceAddForm(request.POST, instance=choice)
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(request, 'Choice updated successfully.', extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:edit_poll', poll.id)
    else:
        form = PollChoiceAddForm(instance=choice)
    return render(request, 'polls/add_choice.html', {'form': form, 'edit_choice': True, 'choice': choice})

@login_required()
def choice_delete(request, choice_id):
    choice = get_object_or_404(PollChoices, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    choice_text = choice.choice_text
    choice.delete()
    messages.success(request, f"Choice ({choice_text}) deleted successfully.", extra_tags='alert alert-success alert-dismissible fade show')
    return redirect('polls:edit_poll', poll.id)


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    user_voted_poll = get_object_or_404(Vote, poll=poll, user=request.user)

    if not poll.active:
        return render(request, 'polls/poll_result.html', {'poll': poll, 'user_voted_poll': user_voted_poll})
    loop_count = poll.pollchoices_set.count()
    return render(request, 'polls/poll_detail.html', {'poll': poll, 'loop_time': range(0, loop_count)})


@login_required()
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice-id')

    if not poll.user_can_vote(request.user):
        messages.error(request, "You've already voted this poll.", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect('polls:list')
    if choice_id:
        choice = get_object_or_404(PollChoices, pk=choice_id)
        vote = Vote(user=request.user, choice=choice, poll=poll)
        vote.save()
        return render(request, 'polls/poll_result.html', {'poll': poll})
    else:
        messages.error(request, 'No Choice selected. Please choose an option first.', extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect('polls:detail_poll', poll.id)

    # return render(request, 'polls/poll_result.html', {'poll': poll})

@login_required()
def end_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    if poll.active:
        poll.active = False
        poll.save()
        return render(request, 'polls/poll_result.html', {'poll': poll})
    else:
        return render(request, 'polls/poll_result.html', {'poll': poll})
