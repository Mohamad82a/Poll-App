from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.contrib import messages
from .models import *

def polls_list(request):
    polls = Poll.objects.all()

    paginator = Paginator(polls, 2)
    page = request.GET.get('page')
    paginated_polls = paginator.get_page(page)

    return render(request, 'polls/polls_list.html', {'polls': paginated_polls})
