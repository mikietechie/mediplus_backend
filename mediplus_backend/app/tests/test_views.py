from django.test import TestCase, client
from django.urls import reverse
from app.models import (
    User, Category, Brand, Cart, CartItem, Watch, PrescribePermission
)
from app.serializers import (
    UserSerializer, CategorySerializer, BrandSerializer, CartSerializer, CartItemSerializer, WatchSerializer, PrescribePermissionSerializer
)

class UserViewTests(TestCase):
    fixtures = ["initial.json"]
    
    @classmethod
    def setUpTestData(cls):
        cls.client = client.Client()
    
    def test_get_user_api_view(self):
        url = reverse('UserAPIView', kwargs={"serializer_data": "data"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(url, data={"paginate": True})
        self.assertEqual(response.status_code, 200)
    
    def test_post_user_api_view(self):
        url = reverse('UserAPIView', kwargs={"serializer_data": "data"})
        data = dict(**UserSerializer(User.objects.first()).data)
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
        data = dict(**UserSerializer(User.objects.first()).data)
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
        
        
        
        

