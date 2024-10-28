from django.contrib import admin
from  .models import CustomUser, Laptop, LaptopReview, SellerReview

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Laptop)
admin.site.register(LaptopReview)
admin.site.register(SellerReview)