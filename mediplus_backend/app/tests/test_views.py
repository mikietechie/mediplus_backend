from django.test import TestCase, client
from django.urls import reverse
from app.models import (
    Company, Category, Product
)
from app.serializers import (
    CompanySerializer, CategorySerializer, ProductSerializer
)
from .create_data import create_models
import json


class TestViews(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        create_models(cls)
        cls.client = client.Client()
    
    def test_company_API_views(self):
        url = reverse('CompanyAPIView')
        #   Test POST method
        response = self.client.post(url, data={'name': 'fifth_company', 'REMOTE_ADDR': 'fifth_company.com'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('name'), 'fifth_company')
        self.assertIsInstance(response.json(), dict)
        #   Now test with invalid data
        response = self.client.post(url, data={'lorem': 'ipsum'})
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response.json(), dict)
        #   Test GET method
        #   NOTE: Initially the companies were 4
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 5)
        #   NOTE: Now change url to the one for put, delete, get(one)
        url = reverse('CompanyActionAPIView', kwargs={'_id': self.company_0.REMOTE_ADDR})
        #   Test GET by id method
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), CompanySerializer(self.company_0).full_data)
        #   Test Put method
        serialized_company_0 = CompanySerializer(self.company_0)
        data = serialized_company_0.data
        data.update({'name': data.get('name').upper()})
        response = self.client.put(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 202) 
        self.assertNotEqual(serialized_company_0.data.get('name'), response.json().get('name'))
        #   Test Delete method
        delete_company = Company.objects.last()
        url = reverse('CompanyActionAPIView', kwargs={'_id': delete_company.REMOTE_ADDR})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(Company.objects.filter(REMOTE_ADDR=delete_company.REMOTE_ADDR).count() == 0)
    
    def test_categoryAPI_views(self):
        url = reverse('CategoryAPIView')
        #   Test POST method
        response = self.client.post(url, data={
            'title': 'category_title',
            'description': 'category_description',
            'company': 'company_0.com',
            'stars': 3,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('title'), 'category_title')
        self.assertIsInstance(response.json(), dict)
        #   Now test with invalid data
        response = self.client.post(url, data={'lorem': 'ipsum'})
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response.json(), dict)
        #   Test GET method
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        #   NOTE: Now change url to the one for put, delete, get(one)
        test_category = Category.objects.first()
        url = reverse('CategoryActionAPIView', kwargs={'_id': test_category.id})
        #   Test GET by id method
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), CategorySerializer(test_category).full_data)
        #   Test Put method
        serialized_category_0 = CategorySerializer(test_category)
        data = serialized_category_0.data
        data.update({'title': data.get('title').upper()})
        response = self.client.put(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 202) 
        self.assertNotEqual(serialized_category_0.data.get('title'), response.json().get('title'))
        #   Test Delete method
        delete_category = Category.objects.last()
        url = reverse('CategoryActionAPIView', kwargs={'_id': delete_category.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(Category.objects.filter(id=delete_category.id).count() == 0)
    
    def test_product_API_views(self):
        url = reverse('ProductAPIView')
        #   Test POST method
        response = self.client.post(url, data={
            'title': 'product_title',
            'description': 'product_description',
            'category': 1,
            'stars': 3,
            'price': 100
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('title'), 'product_title')
        self.assertIsInstance(response.json(), dict)
        #   Now test with invalid data
        response = self.client.post(url, data={'lorem': 'ipsum'})
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response.json(), dict)
        #   Test GET method
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        #   NOTE: Now change url to the one for put, delete, get(one)
        product_0 = Product.objects.first()
        url = reverse('ProductActionAPIView', kwargs={'_id': product_0.id})
        #   Test GET by id method
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), ProductSerializer(product_0).data)
        #   Test Put method
        serialized_product_0 = ProductSerializer(product_0)
        data = serialized_product_0.data
        data.update({'title': data.get('title').upper()})
        response = self.client.put(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 202) 
        self.assertNotEqual(serialized_product_0.data.get('title'), response.json().get('title'))
        #   Test Delete method
        delete_product = Product.objects.last()
        url = reverse('ProductActionAPIView', kwargs={'_id': delete_product.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(Product.objects.filter(id=delete_product.id).count() == 0)
        
        
        
        
        

