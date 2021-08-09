from app.models import (
    User, Category, Brand, Cart, CartItem, Watch, PrescribePermission, Product
)
import datetime


def create_data(cls):
    cls.user = User.objects.create(**{
            "username": "mike",
            "email": "m@m.com",
            "is_staff": True,
            "is_superuser": True,
            "password": "mike1234"
        })
    cls.category_1 = Category.objects.create(**{
            "name": "category 1",
            "description": "category 1 desc"
        })
    cls.category_2 = Category.objects.create(**{
            "name": "category 2",
            "description": "category 2 desc"
        })
    cls.brand_1 = Brand.objects.create(**{
            "name": "brand 1",
            "description": "brand 1 desc"
        })
    cls.brand_2 = Brand.objects.create(**{
            "name": "brand 2",
            "description": "brand 2 desc"
        })
    cls.product_1 = Product.objects.create(**{
            "name": "product 1",
            "description": "product 1 desc",
            "price": 10.00,
            "brand": cls.brand_1,
            "date": datetime.date.today(),
            "quantity": 10
        })
    cls.product_2 = Product.objects.create(**{
            "name": "product 2",
            "description": "product 2 desc",
            "price": 20.00,
            "brand": cls.brand_2,
            "date": datetime.date.today(),
            "quantity": 10
        })
    cls.product_3 = Product.objects.create(**{
            "name": "product 3",
            "description": "product 3 desc",
            "price": 30.00,
            "brand": cls.brand_1,
            "date": datetime.date.today(),
            "quantity": 10
        })
    cls.product_4 = Product.objects.create(**{
            "name": "Chamba",
            "description": "product 4 desc",
            "price": 60.00,
            "brand": cls.brand_1,
            "date": "2003-10-27",
            "requires_prescription": True 
        })
    cls.watch = Watch.objects.create(**{
            "product": cls.product_1,
            "user": cls.user,
            "priority": 3,
            "timestamp": datetime.datetime.now()
        })
    cls.cart = Cart.objects.create(**{
            "name": "my first cart",
            "user": cls.user,
            "timestamp": datetime.datetime.now()
        })
    cls.cart_item_1 = CartItem.objects.create(**{
            "product": cls.product_2,
            "cart": cls.cart,
            "quantity": 1,
            "description": "need it"
        })
    cls.cart_item_2 = CartItem.objects.create(**{
            "product": cls.product_1,
            "cart": cls.cart,
            "quantity": 3,
            "description": "maybe if i have money i will get this"
        })
    cls.prescribe_permission = PrescribePermission.objects.create(**{
            "product": cls.product_4,
            "user": cls.user,
            "quantity": 10,
            "granted_on": datetime.datetime.now(),
            "expires_on": datetime.datetime.max()
        })