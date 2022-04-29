from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Item(models.Model):

    CATEGORY_CHOICES = (
        ('C', 'Casual'),
        ('SW', 'Streetwear'),
        ('EC', 'Esporte-chique'),
    )

    LABEL_CHOICES = (
        ('P', 'primary'),
        ('S', 'secundary'),
        ('D', 'danger'),
    )

    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', args=(self.slug, ))

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', args=(self.slug, ))
    
    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', args=(self.slug, ))

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f'{self.quantity} de {self.item}'

    def get_item_total_price(self):
        return self.quantity * self.item.price


class Address(models.Model):
    street = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    number = models.IntegerField()
    complement = models.CharField(max_length=100)

    def __str__(self):
        return self.street + ' - ' + str(self.number)


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    order_itens = models.ManyToManyField(OrderItem)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_order_total_price(self):
        total_price = 0
        for order_item in self.order_itens.all():
            total_price += order_item.get_item_total_price()

        return total_price