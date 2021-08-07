from django.test import Client, TestCase
from app.models import Company, Category, Product
from .create_data import create_models
from django.db.models import QuerySet

class TestModels(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        create_models(cls)
    
    def test_company_model(self):
        self.assertIsInstance(self.company_0, Company)
        #   self.assertEqual(Company.objects.count(), 4)
        self.assertEqual(self.company_0.__str__(), str(self.company_0))
        self.assertIsInstance(self.company_0.company_categories.all(), QuerySet)
        self.assertIsInstance(self.company_0.get_categories, QuerySet)
        for category in self.company_0.get_categories:
            self.assertIsInstance(category, Category)
    
    def test_category_model(self):
        self.assertIsInstance(self.category_0_company_0, Category)
        #   self.assertEqual(Company.objects.count(), 4)
        self.assertEqual(self.category_0_company_0.__str__(), str(self.category_0_company_0))
        self.assertIsInstance(self.category_0_company_0.category_products.all(), QuerySet)
        self.assertIsInstance(self.category_0_company_0.get_products, QuerySet)
        for product in self.category_0_company_0.get_products:
            self.assertIsInstance(product, Product)
    
    def test_product_model(self):
        self.assertIsInstance(self.product_0_category_0, Product)
        self.assertEqual(self.product_0_category_0.__str__(), str(self.product_0_category_0))
        
        
        
        