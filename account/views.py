from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm


# def register_user(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#
#         if user is not None:
#

def register_user(request):
    check1 = False
    check2 = False
    check3 = False
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        username = form.changed_data['username']
        email = form.changed_data['email']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']

        if password1 != password2:
            check1 = True
            messages.error(request, 'Passwords do not match')


