# Generated by Django 4.2.1 on 2023-08-18 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0007_order_promocode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': False, 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name', 'price'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
    ]