from django.contrib.auth.models import User
from django.shortcuts import render, redirect
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
    if request.method == 'POST':
        check1 = False
        check2 = False
        check3 = False
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password1 != password2:
                check1 = True
                messages.error(request, 'Passwords do not match')

            if User.objects.filter(username=username).exists():
                check2 = True
                messages.error(request, 'Account with this username already exists')

            if User.objects.filter(email=email).exists():
                check3 = True
                messages.error(request, 'Account with this email already exists')

            if check1 and check2 and check3:
                messages.error(request, 'Registration failed! Please try again.')
                return redirect('account:register')

            else:
                User.objects.create_user(username=username, email=email, password=password1)
                messages.success(request, 'Registration was successful!')

                return redirect('account:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Invalid username or password.', extra_tags='alert alert-danger alert-dismissible fade show')
            return redirect('account:login')

    return render(request, 'account/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')
