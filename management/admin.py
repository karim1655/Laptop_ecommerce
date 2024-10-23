from django.contrib import admin
from  .models import CustomUser, Laptop

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Laptop)