from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Address, PromoCode, Order, OrderItem, OrderItemOption, OrderPromo

admin.site.register(Address)
admin.site.register(PromoCode)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderItemOption)
admin.site.register(OrderPromo)