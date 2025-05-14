from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Register view

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered')
            return redirect('register')


        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password1
        )
        login(request, user)
        return redirect('task_list')

    return render(request, 'register.html')


# Login view

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('task_list')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('register')

    return render(request, 'login.html')


# Logout view

def logout_view(request):
    logout(request)
    return redirect('login')
