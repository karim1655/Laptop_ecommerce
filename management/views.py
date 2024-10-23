from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from .forms import *
from .models import CustomUser, Laptop


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'

def home(request):
    return render(request, 'management/home.html')

class LaptopsListView(ListView):
    model = Laptop
    template_name = 'management/laptops_list.html'
    title = 'Laptops list'