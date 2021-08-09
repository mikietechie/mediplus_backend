from django.test import TestCase, client
from django.urls import reverse
from app.models import (
    User, Category, Brand, Cart, CartItem, Watch, PrescribePermission, Product
)
from app.serializers import (
    UserSerializer, CategorySerializer, BrandSerializer, CartSerializer, CartItemSerializer,
    WatchSerializer, PrescribePermissionSerializer, ProductSerializer
)
from .create_test_data import create_data


class UserViewTests(TestCase):
    fixtures = ["initial.json"]
    
    @classmethod
    def setUpTestData(cls):
        cls.client = client.Client()
        #create_data(cls)
    
    def test_get_user_api_view(self):
        url = reverse('UserAPIView', kwargs={"serializer_data": "data"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(url, data={"paginate": True})
        self.assertEqual(response.status_code, 200)
    
    def test_post_user_api_view(self):
        url = reverse('UserAPIView', kwargs={"serializer_data": "data"})
        data = UserSerializer(User.objects.first()).data
        [data.pop(prop) for prop in ["id", "date_joined"]]
        data["username"] = "user"
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        data.pop("username")
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_user_detail_api_view(self):
        url = reverse('UserDetailAPIView', kwargs={"serializer_data": "full_data"})
        response = self.client.get(url, data={"id": 1})
        self.assertEqual(response.status_code, 200)
    
    def test_put_user_detail_api_view(self):
        url = reverse('UserDetailAPIView', kwargs={"serializer_data": "full_data"})
        data = UserSerializer(User.objects.first()).data
        [data.pop(prop) for prop in ["id", "date_joined"]]
        data["username"] = "username"
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 202)

        data.pop("username")
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_user_detail_api_view(self):
        url = reverse('UserDetailAPIView', kwargs={"serializer_data": "data"})
        response = self.client.delete(f"{url}?id=2")
        self.assertEqual(response.status_code, 404)


class CategoryViewTests(TestCase):
    fixtures = ["initial.json"]
    
    @classmethod
    def setUpTestData(cls):
        cls.client = client.Client()
    
    def test_get_category_api_view(self):
        url = reverse('CategoryAPIView', kwargs={"serializer_data": "data"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_category_api_view(self):
        url = reverse('CategoryAPIView', kwargs={"serializer_data": "data"})
        data = CategorySerializer(Category.objects.first()).data
        data.pop("id")
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        data.pop("name")
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_category_detail_api_view(self):
        url = reverse('CategoryDetailAPIView', kwargs={"serializer_data": "full_data"})
        response = self.client.get(url, data={"id": 1})
        self.assertEqual(response.status_code, 200)
    
    def test_put_category_detail_api_view(self):
        url = reverse('CategoryDetailAPIView', kwargs={"serializer_data": "full_data"})
        data = CategorySerializer(Category.objects.first()).data
        data["name"] = "name"
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 202)

        data.pop("name")
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_category_detail_api_view(self):
        url = reverse('CategoryDetailAPIView', kwargs={"serializer_data": "data"})
        response = self.client.delete(f"{url}?id=2")
        self.assertEqual(response.status_code, 204)


class BrandViewTests(TestCase):
    fixtures = ["initial.json"]
    
    @classmethod
    def setUpTestData(cls):
        cls.client = client.Client()
    
    def test_get_brand_api_view(self):
        url = reverse('BrandAPIView', kwargs={"serializer_data": "data"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_brand_api_view(self):
        url = reverse('BrandAPIView', kwargs={"serializer_data": "data"})
        data = BrandSerializer(Brand.objects.first()).data
        [data.pop(prop) for prop in ["logo", "name", "id"]]
        data["name"] = "brand name"
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        data.pop("name")
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_brand_detail_api_view(self):
        url = reverse('BrandDetailAPIView', kwargs={"serializer_data": "full_data"})
        response = self.client.get(url, data={"id": 1})
        self.assertEqual(response.status_code, 200)
    
    def test_put_brand_detail_api_view(self):
        url = reverse('BrandDetailAPIView', kwargs={"serializer_data": "full_data"})
        data = BrandSerializer(Brand.objects.first()).data
        [data.pop(prop) for prop in ["logo", "name", "id"]]
        data["name"] = "brandy name"
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 202)

        data.pop("name")
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_brand_detail_api_view(self):
        url = reverse('BrandDetailAPIView', kwargs={"serializer_data": "data"})
        response = self.client.delete(f"{url}?id=2")
        self.assertEqual(response.status_code, 204)


class ProductViewTests(TestCase):
    fixtures = ["initial.json"]
    
    @classmethod
    def setUpTestData(cls):
        cls.client = client.Client()
    
    def test_get_product_api_view(self):
        url = reverse('ProductAPIView', kwargs={"serializer_data": "data"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_product_api_view(self):
        url = reverse('ProductAPIView', kwargs={"serializer_data": "data"})
        data = ProductSerializer(Product.objects.first()).data
        [data.pop(prop) for prop in ["id"]]
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        data.pop("name")
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_product_detail_api_view(self):
        url = reverse('ProductDetailAPIView', kwargs={"serializer_data": "full_data"})
        response = self.client.get(url, data={"id": 1})
        self.assertEqual(response.status_code, 200)
    
    def test_put_product_detail_api_view(self):
        url = reverse('ProductDetailAPIView', kwargs={"serializer_data": "full_data"})
        data = ProductSerializer(Product.objects.first()).data
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 202)

        data.pop("name")
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_product_detail_api_view(self):
        url = reverse('ProductDetailAPIView', kwargs={"serializer_data": "data"})
        response = self.client.delete(f"{url}?id=2")
        self.assertEqual(response.status_code, 204)


class PrescribePermissionViewTests(TestCase):
    fixtures = ["initial.json"]
    
    @classmethod
    def setUpTestData(cls):
        cls.client = client.Client()
    
    def test_get_prescribe_permission_api_view(self):
        url = reverse('PrescribePermissionAPIView', kwargs={"serializer_data": "data"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_prescribe_permission_api_view(self):
        url = reverse('PrescribePermissionAPIView', kwargs={"serializer_data": "data"})
        data = PrescribePermissionSerializer(PrescribePermission.objects.first()).data
        [data.pop(prop) for prop in ["id"]]
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        data.pop("user")
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_prescribe_permission_detail_api_view(self):
        url = reverse('PrescribePermissionDetailAPIView', kwargs={"serializer_data": "data"})
        response = self.client.get(url, data={"id": 1})
        self.assertEqual(response.status_code, 200)
    
    def test_put_prescribe_permission_detail_api_view(self):
        url = reverse('PrescribePermissionDetailAPIView', kwargs={"serializer_data": "data"})
        data = PrescribePermissionSerializer(PrescribePermission.objects.first()).data
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 202)

        data.pop("user")
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_prescribe_permission_detail_api_view(self):
        url = reverse('PrescribePermissionDetailAPIView', kwargs={"serializer_data": "data"})
        response = self.client.delete(f"{url}?id=1")
        self.assertEqual(response.status_code, 204)


class WatchViewTests(TestCase):
    fixtures = ["initial.json"]
    
    @classmethod
    def setUpTestData(cls):
        cls.client = client.Client()
    
    def test_get_watch_api_view(self):
        url = reverse('WatchAPIView', kwargs={"serializer_data": "data"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_watch_api_view(self):
        url = reverse('WatchAPIView', kwargs={"serializer_data": "data"})
        data = WatchSerializer(Watch.objects.first()).data
        [data.pop(prop) for prop in ["product", "id", "timestamp"]]
        data["product"] = 4
        response = self.client.post(url, data=data, content_type='application/json')
        print(response.content)
        self.assertEqual(response.status_code, 201)
        
        data.pop("user")
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_watch_detail_api_view(self):
        url = reverse('WatchDetailAPIView', kwargs={"serializer_data": "full_data"})
        response = self.client.get(url, data={"id": 1})
        self.assertEqual(response.status_code, 200)
    
    def test_put_watch_detail_api_view(self):
        url = reverse('WatchDetailAPIView', kwargs={"serializer_data": "full_data"})
        data = WatchSerializer(Watch.objects.first()).data
        data["priority"] = 4
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 202)

        data.pop("user")
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_watch_detail_api_view(self):
        url = reverse('WatchDetailAPIView', kwargs={"serializer_data": "data"})
        response = self.client.delete(f"{url}?id=1")
        self.assertEqual(response.status_code, 204)


class CartViewTests(TestCase):
    fixtures = ["initial.json"]
    
    @classmethod
    def setUpTestData(cls):
        cls.client = client.Client()
    
    def test_get_cart_api_view(self):
        url = reverse('CartAPIView', kwargs={"serializer_data": "data"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_cart_api_view(self):
        url = reverse('CartAPIView', kwargs={"serializer_data": "data"})
        data = CartSerializer(Cart.objects.first()).data
        [data.pop(prop) for prop in ["id"]]
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        data.pop("user")
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_cart_detail_api_view(self):
        url = reverse('CartDetailAPIView', kwargs={"serializer_data": "full_data"})
        response = self.client.get(url, data={"id": 1})
        self.assertEqual(response.status_code, 200)
    
    def test_put_cart_detail_api_view(self):
        url = reverse('CartDetailAPIView', kwargs={"serializer_data": "full_data"})
        data = CartSerializer(Cart.objects.first()).data
        data["name"] = 'fd cart'
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 202)

        data.pop("user")
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_cart_detail_api_view(self):
        url = reverse('CartDetailAPIView', kwargs={"serializer_data": "data"})
        response = self.client.delete(f"{url}?id=1")
        self.assertEqual(response.status_code, 204)


class CartItemViewTests(TestCase):
    fixtures = ["initial.json"]
    
    @classmethod
    def setUpTestData(cls):
        cls.client = client.Client()
    
    def test_get_cart_item_api_view(self):
        url = reverse('CartItemAPIView', kwargs={"serializer_data": "data"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_cart_item_api_view(self):
        url = reverse('CartItemAPIView', kwargs={"serializer_data": "data"})
        data = CartItemSerializer(CartItem.objects.first()).data
        [data.pop(prop) for prop in ["id"]]
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        data.pop("cart")
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_cart_item_detail_api_view(self):
        url = reverse('CartItemDetailAPIView', kwargs={"serializer_data": "full_data"})
        response = self.client.get(url, data={"id": 1})
        self.assertEqual(response.status_code, 200)
    
    def test_put_cart_item_detail_api_view(self):
        url = reverse('CartItemDetailAPIView', kwargs={"serializer_data": "full_data"})
        data = CartItemSerializer(CartItem.objects.first()).data
        data["quantity"] = 1
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 202)

        data.pop("cart")
        response = self.client.put(f"{url}?id=1", data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_cart_item_detail_api_view(self):
        url = reverse('CartItemDetailAPIView', kwargs={"serializer_data": "data"})
        response = self.client.delete(f"{url}?id=1")
        self.assertEqual(response.status_code, 204)
