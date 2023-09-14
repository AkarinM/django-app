from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import shop_index, ProductCreateView, ProductsListView, ProductDetailsView, \
    ProductUpdateView, ProductDeleteView, OrdersDetailsView, OrdersUpdateView, OrdersDeleteView, OrdersListView, \
    OrdersCreateView, OrdersDataExportView, ProductViewSet, OrderViewSet, LatestProductsFeed, UserOrdersListView, \
    UserOrdersExportView
    # UserOrderViewSet, UserOrdersExportView

app_name = 'shopapp'

routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)
# routers.register('user-orders1', UserOrderViewSet)


urlpatterns = [
    path('', shop_index, name='shop_index'),
    path('api/', include(routers.urls)),
    path('products-add/', ProductCreateView.as_view(), name='products-add'),
    path('products-list/', ProductsListView.as_view(), name='products-list'),
    path('products-details/<int:pk>/', ProductDetailsView.as_view(), name='products-details'),
    path('products-details/<int:pk>/update/', ProductUpdateView.as_view(), name='products-update'),
    path('products-details/<int:pk>/delete/', ProductDeleteView.as_view(), name='products-delete'),
    path('products/latest/feed/', LatestProductsFeed(), name='products-feed'),
    path('orders-add/', OrdersCreateView.as_view(), name='orders-add'),
    path('orders-list/', OrdersListView.as_view(), name='orders-list'),
    path('orders/export/', OrdersDataExportView.as_view(), name='orders-export'),
    path('orders-details/<int:pk>/', OrdersDetailsView.as_view(), name='orders-details'),
    path('orders-details/<int:pk>/update/', OrdersUpdateView.as_view(), name='orders-update'),
    path('orders-details/<int:pk>/delete/', OrdersDeleteView.as_view(), name='orders-delete'),
    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='user-orders'),
    path('users/<int:user_id>/orders/export/', UserOrdersExportView.as_view(), name='user-orders-export')
]
