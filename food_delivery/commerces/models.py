from django.db import models

# Create your models here.
# commerces/models.py

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

# Import models from the 'catalogs' app
from catalogs.models import Restaurant

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    full_address = models.CharField(max_length=255)
    details = models.CharField(max_length=255, blank=True, help_text="e.g., Apartment, floor, door code")

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.full_address} for {self.user.username}"

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        NEW = 'new', 'New'
        CONFIRMED = 'confirmed', 'Confirmed'
        DELIVERING = 'delivering', 'Delivering'
        DONE = 'done', 'Done'
        CANCELED = 'canceled', 'Canceled'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.NEW)
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    promo_codes = models.ManyToManyField('PromoCode', through='OrderPromo', related_name='orders')
    
    def __str__(self):
        return f"Order #{self.id} for {self.user.username}"

class OrderPromo(models.Model):
    """Through-table for Order and PromoCode."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.PROTECT)
    applied_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    class Meta:
        unique_together = ('order', 'promo_code')

    def __str__(self):
        return f"{self.promo_code.code} applied to Order #{self.order.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255) # Snapshot of MenuItem.name
    item_price = models.DecimalField(max_digits=10, decimal_places=2) # Snapshot of MenuItem.price
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item_name} in Order #{self.order.id}"

class OrderItemOption(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='options')
    option_name = models.CharField(max_length=100) # Snapshot of Option.name
    price_delta = models.DecimalField(max_digits=10, decimal_places=2) # Snapshot of ItemOption.price_delta

    def __str__(self):
        return f"{self.option_name} for {self.order_item.item_name}"