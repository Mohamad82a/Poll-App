from django.urls import path
from . import views
app_name = 'poll_api'

urlpatterns = [
    path('list', views.PollListView.as_view(), name='list'),
    path('detail/<int:pk>', views.PollDetailView.as_view(), name='detail'),
    path('edit/<int:pk>', views.PollEditView.as_view(), name='edit'),
]