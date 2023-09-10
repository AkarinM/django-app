from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Команда для заполнения модели product
    """
    def handle(self, *args, **options):
        from shopapp.models import Product

        Product.objects.get_or_create(name='apple', description='this is a green apple', price=50, count=500)
        Product.objects.get_or_create(name='coffee', description='this is a hot coffee', price=85, count=30)
        Product.objects.get_or_create(name='milk', description='this is milk', price=120, count=100)
