from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    count = models.PositiveSmallIntegerField(default=0)
    changed = models.DateTimeField(auto_now=True)
    arhive = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_product', null=True, default=None)

    class Meta:
        ordering = ['name', 'price']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return f'{self.pk}:  {self.name!r}'

    def get_absolute_url(self):
        return reverse('shopapp:products-details', kwargs={'pk': self.pk})

class Order(models.Model):
    address = models.TextField()
    comment = models.CharField(max_length=150)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_orders', null=True, default=None)
    products = models.ManyToManyField(Product, related_name='orders', default=None)

    class Meta:
        ordering = False
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
