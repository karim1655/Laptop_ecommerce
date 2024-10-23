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

urlpatterns = [
    path('admin/', admin.site.urls, name='Admin'),

    path('', views.home, name='Home'),

    path('register/', views.register, name='Register'),
    path('login/', views.CustomLoginView.as_view(), name='Login'),
    path('logout/', views.CustomLogoutView.as_view(next_page='Home'), name='Logout'),

    path('products/', views.LaptopsListView.as_view(), name='Products'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
