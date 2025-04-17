from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('list', views.polls_list, name='list'),
    path('list_by_user', views.user_polls_list, name='list_by_user'),
    path('addpoll', views.poll_add, name='add_poll'),
    path('editpoll/<int:poll_id>', views.poll_edit, name='edit_poll'),
    path('deletepoll/<int:poll_id>', views.poll_delete, name='delete_poll'),
    path('addchoice/<int:poll_id>', views.choice_add, name='add_choice'),
    path('editchoice/<int:choice_id>', views.choice_edit, name='edit_choice'),
    path('deletechoice/<int:choice_id>', views.choice_delete, name='delete_choice'),
    path('detail/<int:poll_id>', views.poll_detail, name='detail_poll'),
    path('vote/<int:poll_id>', views.poll_vote, name='vote_poll'),
    path('end/<int:poll_id>', views.end_poll, name='end_poll'),
]