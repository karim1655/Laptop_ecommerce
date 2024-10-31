"""
URL configuration for laptop_ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from management import views
from management.views import custom_403_view

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(next_page='home'), name='logout'),

    path('addlaptop', views.add_laptop, name='add_laptop'),
    path('laptopslist/', views.LaptopsListView.as_view(), name='laptops_list'),
    path('laptopdetail/<pk>/', views.LaptopDetailView.as_view(), name='laptop_detail'),
    path('laptopdelete/<pk>/', views.LaptopDeleteView.as_view(), name='laptop_delete'),
    path('laptopupdate/<pk>/', views.LaptopUpdateView.as_view(), name='laptop_update'),

    path('search', views.search, name='search'),

    path('sellerdashboard/<int:seller_id>/', views.seller_dashboard, name='seller_dashboard'),

    path('laptopreview/<int:laptop_id>/', views.add_laptop_review, name='laptop_review'),
    path('laptopdetail/<int:laptop_id>/reviews', views.laptop_and_seller_reviews_list, name='laptop_and_seller_reviews_list'),
    path('sellerreview/<int:seller_id>/<int:laptop_id>', views.add_seller_review, name='seller_review'),


    path('add_to_cart/<int:laptop_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom errors pages
handler403 = custom_403_view