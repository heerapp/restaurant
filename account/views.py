from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


def signup(request):
    if request.method == 'POST':
        # user has info and wants an account now!
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'account/signup.html'), {'error': 'Username has already been taken'}
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                auth.login(request, user)
                return redirect('/')
        else:
            return render(request, 'account/signup.html'), {'error': 'Passwords should match'}

    else:
        # user wants to enter info
        return render(request, 'account/signup.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            if request.user.is_superuser:
                return redirect('/allorders/')
            elif request.user.is_staff:
                return redirect('/tables/')
            else:
                return redirect('/')
        else:
            return render(request, 'account/login.html', {'error': 'username or password is incorrect.'})

    else:
        return render(request, 'account/login.html')

