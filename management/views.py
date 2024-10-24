from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
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

def add_laptop(request):
    if request.method == 'POST':
        form = LaptopForm(request.POST, request.FILES)
        if form.is_valid():
            laptop = form.save(commit=False)
            laptop.seller = request.user
            laptop.save()
            messages.success(request, 'Laptop created successfully')
            return redirect('LaptopsList')
        else:
            messages.error(request, 'Laptop not created')
    else:
        form = LaptopForm()
    return render(request, 'management/add_laptop.html', {'form': form})

class LaptopDetailView(DetailView):
    model = Laptop
    template_name = 'management/laptop_detail.html'

class LaptopDeleteView(DeleteView):
    model = Laptop
    template_name = 'management/laptop_delete.html'
    success_url = reverse_lazy('LaptopsList')

class LaptopUpdateView(UpdateView):
    model = Laptop
    template_name = 'management/laptop_update.html'
    form_class = LaptopForm

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("LaptopDetail", kwargs={'pk': pk})