from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache

from shopapp.models import Product, Order
from shopapp.serializes import ProductSerializer, OrderSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = [
        'name',
        'description',
    ]
    ordering_fields = [
        'pk',
        'name',
        'price',
        'discount',
        'count',
        'changed',
        'arhive',
        'created_by',
    ]


class UserOrdersExportView(PermissionRequiredMixin, View):
    permission_required = ['shopapp.view_order']

    def get(self, request, user_id) -> JsonResponse:
        cache_key = f'orders_usrid_{user_id}'
        orders = cache.get(cache_key)

        if orders is None:
            if not User.objects.filter(pk=user_id).exists():
                raise Http404

            orders = Order.objects.prefetch_related('products').select_related('user').all()
            cache.set(cache_key, list(orders), 60)

        serializer = OrderSerializer(orders, many=True)

        return JsonResponse({'orders': serializer.data})


# class UserOrderViewSet(ModelViewSet):
#     queryset = Order.objects.prefetch_related('products').select_related('user').all()
#     serializer_class = OrderSerializer
#     lookup_field = 'user_id'
#
#     @action(methods=['get'], detail=True)
#     def list_user_orders(self, request, user_id=None):
#         cache_key = f'orders_usrid_{user_id}'
#         queryset = cache.get(cache_key)
#
#         if queryset is None:
#             if not User.objects.filter(pk=user_id).exists():
#                 raise Http404
#
#             queryset = self.queryset.filter(user_id=user_id).order_by('pk')
#             cache.set(cache_key, list(queryset), 60)
#
#         serializer = self.get_serializer(queryset, many=True)
#
#         return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related('products').select_related('user').all()
    serializer_class = OrderSerializer

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = [
        'address',
        'comment',
        'promocode',
        'created',
        'user',
        'products',

    ]
    ordering_fields = [
        'pk',
        'address',
        'created',
        'user',
        'products',
    ]

def shop_index(request: HttpRequest) -> HttpResponse:
    """
    Отображает страницу shop_index
    :param request: request
    :return: html - страница
    """

    return render(request, 'shopapp/shop_index.html', context={})


class ProductsListView(ListView):
    template_name = 'shopapp/products_list.html'
    queryset = Product.objects.filter(arhive=False)
    context_object_name = 'products'


class LatestProductsFeed(Feed):
    title = 'Products feed'
    descriptions = 'This is Products feed'
    link = reverse_lazy('shopapp:products-list')

    def items(self):
        return Product.objects.filter(arhive=False)[:5]

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:30]

    # def item_link(self, item: Product):
    #     return reverse('shopapp:products-details', kwargs={'pk': item.pk})


class ProductDetailsView(DetailView):
    template_name = 'shopapp/product_details.html'
    model = Product
    context_object_name = 'product'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ['shopapp.add_product']
    model = Product
    fields = 'name', 'description', 'price', 'discount', 'count'
    template_name_suffix = '_add'
    success_url = reverse_lazy('shopapp:products-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)

        return response


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        user = self.request.user
        return user.has_perm('shopapp.change_product') and \
            self.get_object().created_by == user

    model = Product
    fields = 'name', 'description', 'price', 'discount', 'count'
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse('shopapp:products-details', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products-list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.arhive = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/user_orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self) -> QuerySet:
        user_id = self.kwargs['user_id']
        orders = Order.objects.select_related('user').prefetch_related('products').filter(user__pk=user_id)

        try:
            self.owner = orders[0].user
        except IndexError:
            try:
                self.owner = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                raise Http404

        return orders

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner

        return context


class OrdersListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/orders_list.html'
    queryset = Order.objects.select_related('user').prefetch_related('products')
    context_object_name = 'orders'


class OrdersDetailsView(DetailView):
    template_name = 'shopapp/order_details.html'
    queryset = Order.objects.select_related('user').prefetch_related('products')
    context_object_name = 'order'


class OrdersCreateView(CreateView):
    model = Order
    fields = 'address', 'comment', 'user', 'products'
    template_name_suffix = '_add'
    success_url = reverse_lazy('shopapp:orders-list')


class OrdersUpdateView(UpdateView):
    model = Order
    fields = 'address', 'comment', 'user', 'products'
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse('shopapp:orders-details', kwargs={'pk': self.object.pk})


class OrdersDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders-list')


class OrdersDataExportView(PermissionRequiredMixin, View):
    permission_required = ['shopapp.view_order']

    def get(self, request) -> JsonResponse:
        orders = Order.objects.prefetch_related('products').order_by('pk').all()
        orders_data = [
            {
                'pk': order.pk,
                'address': order.address,
                'comment': order.comment,
                'promocode': order.promocode,
                'user': order.user_id,
                'products': [product.pk for product in order.products.all()],
            }
            for order in orders
        ]

        return JsonResponse({'orders': orders_data})

