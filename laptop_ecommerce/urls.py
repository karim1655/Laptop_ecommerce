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
    path('admin/', admin.site.urls, name='Admin'),

    path('', views.home, name='Home'),

    path('register/', views.register, name='Register'),
    path('login/', views.CustomLoginView.as_view(), name='Login'),
    path('logout/', views.CustomLogoutView.as_view(next_page='Home'), name='Logout'),

    path('addlaptop', views.add_laptop, name='AddLaptop'),
    path('laptopslist/', views.LaptopsListView.as_view(), name='LaptopsList'),
    path('laptopdetail/<pk>/', views.LaptopDetailView.as_view(), name='LaptopDetail'),
    path('laptopdelete/<pk>/', views.LaptopDeleteView.as_view(), name='LaptopDelete'),
    path('laptopupdate/<pk>/', views.LaptopUpdateView.as_view(), name='LaptopUpdate'),

    path('search', views.search, name='Search'),

    path('sellerdashboard/<int:seller_id>/', views.seller_dashboard, name='SellerDashboard'),

    path('laptopreview/<int:laptop_id>/', views.add_laptop_review, name='LaptopReview'),
    path('laptopdetail/<int:laptop_id>/reviews', views.laptop_and_seller_reviews_list, name='LaptopAndSellerReviewsList'),
    path('sellerreview/<int:seller_id>/<int:laptop_id>', views.add_seller_review, name='SellerReview'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom errors pages
handler403 = custom_403_view