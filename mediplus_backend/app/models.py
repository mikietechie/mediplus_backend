from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
import datetime

#   Exceptions
class PrescriptionException(Exception): pass

class QuantityException(Exception): pass

class CheckoutException(Exception): pass

class CartClosedException(Exception): pass

#   Abstract models
class HasStars(models.Model):
    stars = models.IntegerField(default=3, db_index=True)

    class Meta:
        abstract = True
        ordering = ['stars']

class HasName(models.Model):
    name = models.CharField(max_length=128, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class HasDate(models.Model):
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


#   Modified models fields
class ImageField(models.ImageField):
    @property
    def url(*args, **kwargs):
        try:
            return super().url
        except:
            return None


class FileField(models.FileField):
    @property
    def url(*args, **kwargs):
        try:
            return super().url
        except:
            return None


class MoneyField(models.FloatField):
    def get_prep_value(self, value):
        value = super().get_prep_value(self, value)
        if isinstance(value, float):
            return round(value, 2)
        return value


#### models ####
class User(AbstractUser):
    
    @property
    def carts(self): return self.user_carts.all()
    
    @property
    def watches(self): return self.user_watch_list.all()
    
    @property
    def prescriptions(self): return self.user_prescribe_permissions.all()


class Category(HasName, HasStars):
    """Model definition for Category."""
    description = models.TextField(max_length=516)
    image = ImageField(upload_to=f'categories', blank=True, null=True)
    
    @property
    def products(self): return self.category_products.filter(stars__gte = 3)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['stars']


class Brand(HasName, HasStars):
    logo = models.URLField(max_length=10024)
    description = models.TextField(max_length=516, blank=True, null=True)

    @property
    def products(self): return self.brand_products.filter(stars__gte=3)

    class Meta:
        ordering = ['-stars','name']
        verbose_name = ("Brand")
        verbose_name_plural = ("Brands")


class Product(HasName, HasStars):
    """Model defination for Product"""
    code = models.CharField(max_length=64, blank=True, null=True)
    price = models.FloatField(default=0.0)
    description = models.TextField(max_length=516, blank=True, null=True)
    image = ImageField(upload_to=f"products", blank=True, null=True)
    category = models.ManyToManyField(Category, related_name="category_products", blank=True)
    brand = models.ForeignKey(Brand, related_name='brand_products', blank=True, null=True, on_delete=models.CASCADE)
    parent = models.ManyToManyField("self", related_name="product_products", blank=True)
    sibling = models.ManyToManyField("self", related_name="product_siblings", blank=True)
    discount = models.FloatField(default=0)
    date = models.DateField(auto_now=True)
    for_sale = models.BooleanField(default=True)
    is_parent_only = models.BooleanField(default=False)
    requires_prescription = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=0)
        
    class Meta:
        ordering = ['-stars', 'name']
    
    def save(self,*args, **kwargs):
        self.price = round(self.price, 2)
        super().save(*args, **kwargs)
    
    @property
    def categories(self): return self.category.all()
    
    @property
    def siblings(self): return self.sibling.all()
    
    @property
    def parents(self): return self.parent.all()
    
    @property
    def has_parent(self): return self.parent.count() > 0

    @property
    def selling_price(self): return self.price - self.discount


class PrescribePermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_prescribe_permissions")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_prescribe_permissions")
    granted_on = models.DateTimeField(auto_created=True)
    expires_on = models.DateTimeField()
    quantity = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.product.requires_prescription:
            raise Exception("No need to create a prescription permission for a product that does not have a prescription required attribute")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.product}"

####    E Commerce Models   ####
class Watch(models.Model):
    product = models.ForeignKey(Product, related_name="product_watches", on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, related_name="user_watch_list", on_delete=models.CASCADE)
    priority = models.IntegerField(choices=[(i,i) for i in range(5)])
    timestamp = models.DateTimeField("Created on", auto_now_add=True)

    def __str__(self): return f"{self.user} watching {self.item}"

    class Meta:
        verbose_name = "Watch"
        verbose_name_plural = "Watches"
        order_with_respect_to = "user"
        unique_together = [
            ["user", "product"]
        ]

    
class Cart(HasName):
    cart_statuses = (
        ("active", "active"),
        ("checked out", "checked out"),
        ("paid", "paid"),
        ("delivered", "delivered")

    )
    user = models.ForeignKey(User, related_name="user_carts", on_delete=models.CASCADE)
    timestamp = models.DateTimeField('Created on', auto_now_add=True)
    status = models.CharField(max_length=64, default="active")

    def copy_cart(self):
        new_cart = Cart.objects.create(name=self.name, user=self.user)
        for cart_item in self.cart_items:
            CartItem.objects.create(description=cart_item.description, product=cart_item.product, cart=new_cart, quantity=cart_item.quantity)
        return new_cart

    @property
    def cart_items(self): return self.items.all()

    @property
    def items_count(self): return self.cart_items.count()

    @property
    def total(self): return sum([item.price for item in self.cart_items])
    
    def can_check_out(self):
        for cart_item in self.cart_items:
            if cart_item.quantity > cart_item.product.quantity:
                raise QuantityException(f"Insufficient items in stock")
            if cart_item.product.requires_prescription:
                try:
                    PrescribePermission.objects.get(
                        user=self.user, product=cart_item.product,
                        expires_on__lte=datetime.datetime.now(), quantity__gte=cart_item.quantity
                    )
                except: raise PrescriptionException("Prescription is exhausted or expired!")
        return True
    
    def checkout(self):
        try:
            self.can_check_out()
            #   checkout
        except:
            raise CheckoutException("Checkout failed due to prescription issues or exhausted quantity")
    

    class Meta:
        order_with_respect_to = "user"

    
class CartItem(models.Model):
    product = models.ForeignKey(Product, related_name="cart_item_products", on_delete=models.CASCADE, blank=True, null=True)
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    description = models.TextField(max_length=256, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.cart.status != "active":
            raise CartClosedException("Cart no longer active!")
        if self.product.requires_prescription:
            try:
                prescribe_permission = PrescribePermission.objects.get(
                    user=self.cart.user, product=self.product,
                    expires_on__lte=datetime.datetime.now(), quantity__gte=self.quantity
                )
                prescribe_permission.quantity -= self.quantity
                prescribe_permission.save()
            except:
                raise PrescriptionException("Sold on prescription only!")
        if self.quantity > self.product.quantity:
            raise QuantityException("Insufficient products in stock!!!")
        for cart_item in self.cart.cart_items:
            if cart_item.item.pk == self.item.pk:
                return CartItem.objects.filter(pk=cart_item.pk).update(quantity = self.quantity, description = self.description)
        super().save(self, *args, **kwargs)

    def __str__(self): return f"{self.product} {self.quantity}"

    @property
    def price(self): return self.item.selling_price * self.quantity