from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, LaptopForm, SearchForm
from .models import CustomUser, Laptop
from .decorators import seller_required, SellerRequiredMixin


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

@login_required
@seller_required
def add_laptop(request):
    if request.method == 'POST':
        form = LaptopForm(request.POST, request.FILES)
        if form.is_valid():
            laptop = form.save(commit=False)
            laptop.seller = request.user
            laptop.save()
            messages.success(request, 'Laptop created successfully')

            seller_id = request.user.id
            return redirect('SellerDashboard', seller_id)
        else:
            messages.error(request, 'Laptop not created')
    else:
        form = LaptopForm()
    return render(request, 'management/add_laptop.html', {'form': form})

class LaptopDetailView(DetailView):
    model = Laptop
    template_name = 'management/laptop_detail.html'

class LaptopDeleteView(SellerRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Laptop
    template_name = 'management/laptop_delete.html'
    def get_success_url(self):
        seller_id = self.request.user.id
        return reverse('SellerDashboard', kwargs={'seller_id': seller_id})

class LaptopUpdateView(SellerRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Laptop
    template_name = 'management/laptop_update.html'
    form_class = LaptopForm

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("LaptopDetail", kwargs={'pk': pk})


def search(request):
    ctx = None

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            processor_model = form.cleaned_data.get("processor_model")
            ram = form.cleaned_data.get("ram")
            storage = form.cleaned_data.get("storage")
            display_inches = form.cleaned_data.get("display_inches")
            price = form.cleaned_data.get("price")
            category = form.cleaned_data.get("category")

            laptops = Laptop.objects.all()
            if name:
                laptops = laptops.filter(name__icontains=name)
            if processor_model:
                laptops = laptops.filter(processor_model__iexact=processor_model)
            if ram:
                laptops = laptops.filter(ram__iexact=ram)
            if storage:
                laptops = laptops.filter(storage__iexact=storage)
            if display_inches:
                laptops = laptops.filter(display_inches__iexact= display_inches)
            if price:
                laptops = laptops.filter(price__lte=price)
            if category:
                laptops = laptops.filter(category__icontains=category)

            ctx = {
                'form': form,
                'laptops': laptops,
            }

    return render(request, 'management/search.html', ctx)


@login_required
@seller_required
def seller_dashboard(request, seller_id):
    ctx = {
        "object_list" : Laptop.objects.filter(seller=seller_id),
    }
    return render(request, 'management/seller_dashboard.html', context=ctx)