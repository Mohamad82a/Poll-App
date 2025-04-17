from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('list', views.polls_list, name='list'),
    path('list_by_user', views.user_polls_list, name='list_by_user'),
    path('add', views.poll_add, name='add_poll'),
    path('edit/<int:poll_id>', views.poll_edit, name='edit_poll'),
]