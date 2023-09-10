from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Команда для заполнения модели product
    """
    def handle(self, *args, **options):
        from shopapp.models import Order
        from shopapp.models import Product
        from django.contrib.auth.models import User

        order, created = Order.objects.get_or_create(
            address='st. Lenina, 5, 39',
            comment='As quickly as possible, please',
            user=User.objects.get(username='admin'),
        )

        if created:
            order.products.set(list(Product.objects.filter(arhive=False)))
