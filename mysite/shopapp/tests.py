from django.contrib.auth import login
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Order


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='testuser', password='qwerty')
        cls.user = User.objects.create_user(**cls.credentials)
        # perm = Permission.objects.get_by_natural_key('view_order', 'shopapp', 'order')
        cls.user.user_permissions.add(Permission.objects.get_by_natural_key('view_order', 'shopapp', 'order'))

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)

        self.order = Order.objects.create(
            address='blablabla',
            comment='loooooooong comment',
            promocode='',
            user=self.user,
        )

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse('shopapp:orders-details', kwargs={'pk': self.order.pk}))
        order_ = response.context['order']

        self.assertEquals(self.order.pk, order_.pk)

        self.assertContains(response, 'Comment')
        self.assertContains(response, 'Promocode')


class OrdersExportTestCase(TestCase):
    fixtures = [
        'content_types-fixture.json',
        'permissions-fixture.json',
        'groups-fixture.json',
        'users-fixture.json',
        'products-fixture.json',
        'orders-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        ContentType.objects.all().delete()
        ContentType.objects._cache = dict()
        super().setUpClass()
        cls.credentials = dict(username='testuser', password='qwerty')
        cls.user = User.objects.create_user(**cls.credentials)
        cls.user.user_permissions.add(Permission.objects.get_by_natural_key('view_order', 'shopapp', 'order'))

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)

    def test_get_orders_view(self):
        response = self.client.get(reverse('shopapp:orders-export'))

        self.assertEquals(response.status_code, 200)

        orders = Order.objects.prefetch_related('products').order_by('pk').all()
        expected_data = [
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

        orders_data = response.json()
        self.assertEquals(orders_data['orders'], expected_data)
