from django.db import models

# Create your models here.
# catalogs/models.py

from django.db import models
from django.core.validators import MinValueValidator

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )
    is_available = models.BooleanField(default=True)
    categories = models.ManyToManyField('Category', through='ItemCategory', related_name='menu_items')
    options = models.ManyToManyField('Option', through='ItemOption', related_name='menu_items')

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class ItemCategory(models.Model):
    """Through-table for MenuItem and Category."""
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        # Ensures an item cannot be in the same category twice
        unique_together = ('menu_item', 'category')
        ordering = ['position']

    def __str__(self):
        return f"{self.menu_item.name} in {self.category.name}"

class Option(models.Model):
    name = models.CharField(max_length=100) # e.g., "Size", "Cheese"

    def __str__(self):
        return self.name

class ItemOption(models.Model):
    """Through-table for MenuItem and Option."""
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    price_delta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Price adjustment for this option. Can be negative."
    )
    is_default = models.BooleanField(default=False)

    class Meta:
        # Ensures an item cannot have the same option twice
        unique_together = ('menu_item', 'option')

    def __str__(self):
        return f"{self.option.name} for {self.menu_item.name}"