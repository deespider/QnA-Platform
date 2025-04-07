from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm

class RegisterAPIView(APIView):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('question_list_create')  # Redirect to feed
            form.add_error('username', 'Username already exists or invalid registration.')
        return render(request, 'register.html', {'form': form,})

class LoginAPIView(APIView):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('question_list_create')  # Redirect to feed
            form.add_error(None, 'Invalid username or password.')
        return render(request, 'login.html', {'form': form,})