from django.contrib import admin
from  .models import CustomUser, Laptop, LaptopReview, SellerReview, Cart, CartItem, Order, OrderItem

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Laptop)
admin.site.register(LaptopReview)
admin.site.register(SellerReview)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)