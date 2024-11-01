from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from numpy.ma.extras import average

from .forms import CustomUserCreationForm, LaptopForm, SearchForm, LaptopReviewForm, SellerReviewForm
from .models import CustomUser, Laptop, LaptopReview, SellerReview, Cart, CartItem, Order, OrderItem
from .decorators import seller_required, SellerRequiredMixin
from .recommendations import get_recommendations
from django.db.models import Avg, Sum, F


# Create your views here.

def custom_403_view(request, exception):
    return render(request, 'management/403.html', status=403)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'


def home(request):
    recommended_laptops = get_recommendations(request.user)
    most_highly_rated = Laptop.objects.annotate(
        avg = Avg('laptopreview__rating')
    ).order_by('-avg')[:6]
    return render(request, 'management/home.html', {'recommended_laptops': recommended_laptops, 'most_highly_rated': most_highly_rated})


class LaptopsListView(ListView):
    model = Laptop
    template_name = 'management/laptops_list.html'
    title = 'Laptops list'

    def get_queryset(self):
        return Laptop.objects.order_by('seller')

@login_required
@seller_required
def add_laptop(request):
    if request.method == 'POST':
        form = LaptopForm(request.POST, request.FILES)
        if form.is_valid():
            laptop = form.save(commit=False)
            laptop.seller = request.user
            laptop.save()
            messages.success(request, 'Laptop aggiunto con successo')

            seller_id = request.user.id
            return redirect('seller_dashboard', seller_id)
        else:
            messages.error(request, 'Laptop non creato')
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
        return reverse('seller_dashboard', kwargs={'seller_id': seller_id})

class LaptopUpdateView(SellerRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Laptop
    template_name = 'management/laptop_update.html'
    form_class = LaptopForm

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("laptop_detail", kwargs={'pk': pk})


def search(request):
    ctx = None

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            processor_brand = form.cleaned_data.get("processor_brand")
            ram = form.cleaned_data.get("ram")
            storage = form.cleaned_data.get("storage")
            display_inches = form.cleaned_data.get("display_inches")
            price = form.cleaned_data.get("price")
            category = form.cleaned_data.get("category")

            laptops = Laptop.objects.all()
            if name:
                laptops = laptops.filter(name__icontains=name)
            if processor_brand:
                laptops = laptops.filter(processor_brand__iexact=processor_brand)
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
    seller_reviews = SellerReview.objects.filter(seller_id=seller_id)

    # Stats vendite
    total_sales = OrderItem.objects.filter(laptop__seller=seller_id).aggregate(
        total_sales = Sum(F('price') * F('quantity'))
    )['total_sales'] or 0
    total_sales = round(total_sales, 2)

    total_orders = OrderItem.objects.filter(laptop__seller=seller_id).aggregate(
        total_quantity_sold=Sum('quantity')
    )['total_quantity_sold'] or 0

    top_selling_laptops = (Laptop.objects.filter(seller_id=seller_id, orderitem__isnull=False)
        .annotate(total_sold=Sum('orderitem__quantity'))
        .order_by('-total_sold'))

    ctx = {
        "object_list" : Laptop.objects.filter(seller=seller_id),
        "seller_reviews": seller_reviews,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'top_selling_laptops': top_selling_laptops,
    }
    return render(request, 'management/seller_dashboard.html', context=ctx)


@login_required
def add_laptop_review(request, laptop_id):
    if request.user.user_type != 'buyer':
        messages.error(request, 'I fornitori non posso aggiungere recensioni ai laptop')
        return redirect('home')
    laptop = get_object_or_404(Laptop, id=laptop_id)
    if LaptopReview.objects.filter(laptop=laptop, user=request.user).exists():
        messages.error(request, 'Hai già recensito questo laptop.')
        return redirect('laptop_detail', laptop_id)

    if request.method == 'POST':
        form = LaptopReviewForm(request.POST)
        if form.is_valid():
            laptop_review = form.save(commit=False)
            laptop_review.user = request.user
            laptop_review.laptop = laptop
            laptop_review.save()
            messages.success(request, 'Recensione al laptop creata con successo')
            return redirect('laptop_detail', laptop_id)
    else:
        form = LaptopReviewForm()
    return render(request, 'management/laptop_review.html', {'form': form, 'laptop_id': laptop_id})

@login_required
def laptop_and_seller_reviews_list(request, laptop_id):
    laptop = get_object_or_404(Laptop, id=laptop_id)
    seller = get_object_or_404(CustomUser, id=laptop.seller_id)
    return render(request, 'management/laptop_and_seller_reviews_list.html', {'laptop': laptop, 'seller': seller})


@login_required
def add_seller_review(request, seller_id, laptop_id):
    if request.user.user_type != 'buyer':
        messages.error(request, 'I fornitori non posso aggiungere recensioni ai fornitori')
        return redirect('home')
    seller = get_object_or_404(CustomUser, id=seller_id)
    if request.method == 'POST':
        form = SellerReviewForm(request.POST)
        if form.is_valid():
            seller_review = form.save(commit=False)
            seller_review.user = request.user
            seller_review.seller = seller
            seller_review.save()
            messages.success(request, 'Recensione al fornitore creata con successo')
            return redirect('laptop_detail', laptop_id)
    else:
        form = SellerReviewForm()
    return render(request, 'management/seller_review.html', {'form': form, 'seller': seller, 'laptop_id': laptop_id})


@login_required
def add_to_cart(request, laptop_id):
    if request.user.user_type != 'buyer':
        messages.error(request, 'I fornitori non possono aggiungere laptop al carrello')
        return redirect('home')

    laptop = get_object_or_404(Laptop, id=laptop_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, laptop=laptop)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Laptop aggiunto al carrello con successo.")
    return redirect('laptop_detail', laptop_id)

@login_required
def cart_detail(request):
    if request.user.user_type != 'buyer':
        messages.error(request, 'I fornitori non possono accedere al carrello')
        return redirect('home')

    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.cartitem_set.all() if cart else []
    return render(request, 'management/cart_detail.html', {'cart_items': cart_items})


@login_required
def increase_quantity(request, item_id):
    if request.user.user_type != 'buyer':
        messages.error(request, 'I fornitori non possono aumentare di quantità un elemento del carrello')
        return redirect('home')

    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

@login_required
def decrease_quantity(request, item_id):
    if request.user.user_type != 'buyer':
        messages.error(request, 'I fornitori non possono diminuire di quantità un elemento del carrello')
        return redirect('home')

    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    if request.user.user_type != 'buyer':
        messages.error(request, 'I fornitori non possono rimuovere un elemento dal carrello')
        return redirect('home')

    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Elemento rimosso dal carrello con successo")
    return redirect('cart_detail')


@login_required
def checkout(request):
    if request.user.user_type != 'buyer':
        messages.error(request, 'I fornitori non possono accedere al checkout')
        return redirect('home')

    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.cartitem_set.exists():
        messages.error(request, "Il carrello è vuoto")
        return redirect('cart_detail')

    cart_items = cart.cartitem_set.all()
    total_amount = sum(item.laptop.price * item.quantity for item in cart_items)
    return render(request, 'management/checkout.html', {'cart_items': cart_items, 'total_amount': total_amount})


@login_required
def confirm_order(request):
    if request.user.user_type != 'buyer':
        messages.error(request, 'I fornitori non possono accedere all\'ordine')
        return redirect('home')

    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.cartitem_set.exists():
        messages.error(request, "Il carrello è vuoto")
        return redirect('checkout')

    cart_items = cart.cartitem_set.all()
    total_amount = sum(item.laptop.price * item.quantity for item in cart_items)
    order = Order.objects.create(user=request.user, total_amount=total_amount, is_paid=False)

    for item in cart_items:
        OrderItem.objects.create(order=order, laptop=item.laptop, quantity=item.quantity, price=item.laptop.price)

    cart.cartitem_set.all().delete()
    messages.success(request, "Ordine confermato con successo")
    return redirect('home')
