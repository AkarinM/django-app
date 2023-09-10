from io import TextIOWrapper

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from .models import Product, Order
from .forms import CSVImportForm

from csv import DictReader, DictWriter


class OrderInLIne(admin.StackedInline):
    model = Product.orders.through


@admin.action(description='Archive products')
def mark_archived(modelAdmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(arhive=True)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [
        mark_archived,
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'count', 'changed', 'arhive'
    list_display_links = 'pk', 'name'
    inlines = [
        OrderInLIne,
    ]
    fieldsets = (
        (None, {
            'fields': ('name', 'description'),
        }),
        ('price options', {
            'fields': ('price','discount'),
            'classes': ('collapse',)
        }),
        ('other', {
            'fields': ('arhive',),
            'classes': ('wide', 'collapse'),
            'description': 'Field "arhive" is for soft delete'
        })
    )

    ordering = 'name', 'price'
    search_fields = 'name', 'pk'

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 20:
            return obj.description
        else:
            return obj.description[:20] + '...'

class ProductInLIne(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = 'shopapp/orders_changelist.html'
    list_display = 'pk', 'address', 'comment', 'created', 'user_verbose'
    list_display_links = 'pk', 'address'
    inlines = [
        ProductInLIne,
    ]

    ordering = '-created',
    search_fields = 'address', 'pk'

    def get_queryset(self, request) -> QuerySet:
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context)

        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context, status=400)

        csv_file = TextIOWrapper(
            form.files['csv_file'].file,
            encoding=request.encoding,
        )

        reader = DictReader(csv_file)

        orders = list()
        products_list = list()
        for row in reader:
            order_obj = Order()
            for k, v in row.items():
                if k != 'products':
                    setattr(order_obj, k, v)
                else:
                    products_list.append(v.replace('[', '').replace(']', '').split(','))
            orders.append(order_obj)

        orders = Order.objects.bulk_create(orders)

        for ord in orders:
            for prod in products_list:
                ord.products.add(*prod)
            ord.save()

        self.message_user(request, 'Data from CSV was imported!')
        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                'import-orders-csv/',
                self.import_csv,
                name='import_orders_csv'
            ),
        ]
        return new_urls + urls
