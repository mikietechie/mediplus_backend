from rest_framework.serializers import ModelSerializer, Serializer
from . models import (
    Category, Brand, Product, Watch, Cart, CartItem, User, PrescribePermission
)
from rest_framework.utils.serializer_helpers import ReturnDict


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    @property
    def full_data(self):
        return ReturnDict(
            {
                **self.data,
                'carts': [CartSerializer(cart).data for cart in self.instance.carts],
                "watches": [WatchSerializer(watch).data for watch in self.instance.watches]
            },
            serializer=self
        )


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    @property
    def full_data(self):
        return ReturnDict(
            {
                **self.data,
                'brand': BrandSerializer(self.instance.brand).data,
                'categories': [CategorySerializer(category).data for category in self.instance.categories],
                "siblings": [ProductSerializer(sibling).data for sibling in self.instance.siblings],
                "parents": [ProductSerializer(parent).data for parent in self.instance.parents],
                "selling_price": self.instance.selling_price
            },
            serializer=self
        )


class PrescribePermissionSerializer(ModelSerializer):
    class Meta:
        model = PrescribePermission
        fields = '__all__'

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
    @property
    def full_data(self):
        return ReturnDict(
            {
                **self.data,
                'products': [ProductSerializer(product).data for product in self.instance.products]
            },
            serializer=self
        )


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
    
    @property
    def full_data(self):
        return ReturnDict(
            {
                **self.data,
                'products': [ProductSerializer(product).data for product in self.instance.products]
            },
            serializer=self
        )


class WatchSerializer(ModelSerializer):
    class Meta:
        model = Watch
        fields = '__all__'
    
    @property
    def full_data(self):
        return ReturnDict(
            {
                **self.data,
                "product": ProductSerializer(self.instance.product).full_data
            },
            serializer=self
        )


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
    
    @property
    def full_data(self):
        return ReturnDict(
            {
                **self.data,
                "items": [CartItemSerializer(cart_item).full_data for cart_item in self.instance.cart_items],
                'total': self.instance.total,
                'items_count': self.instance.items_count
            },
            serializer=self
        )
    
    @property
    def mini_data(self):
        return ReturnDict(
            {
                **self.data,
                'total': self.instance.total,
                'items_count': self.instance.items_count
            },
            serializer=self
        )


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
    
    @property
    def full_data(self):
        return ReturnDict(
            {
                **self.data,
                'product': dict(
                    id=self.instance.product.id,
                    code=self.instance.product.code,
                    name=self.instance.product.name,
                    image=self.instance.product.image.url, 
                    price=self.instance.product.price,
                    discount=self.instance.product.discount,
                    selling_price=self.instance.product.selling_price,
                    brand=str(self.instance.product.brand)
                ),
                'price': self.instance.price
            },
            serializer=self
        )