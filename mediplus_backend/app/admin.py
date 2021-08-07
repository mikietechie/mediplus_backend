from django.contrib import admin
from app.models import (
    Category,
    Brand,
    Product,
    User,
    Cart,
    Watch,
    CartItem,
    PrescribePermission
)


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    ordering = ['username']

    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'stars']
    list_filter = ['stars']
    ordering = ['name', 'stars']

    
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'stars']
    list_filter = ['stars']
    ordering = ['name', 'stars']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stars']
    list_filter = ['is_parent_only', 'for_sale']
    ordering = ['name','stars']
    list_per_page = 300


@admin.register(PrescribePermission)
class PrescribePermissionAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "expires_on", "quantity"]


#### E Commerce models admin    ####
@admin.register(Cart)
class CartAdmn(admin.ModelAdmin):
    list_display = ["user", "name", "timestamp", "total"]
    list_filter = ["user"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity", "cart"]
    list_filter = ["product", "quantity", "cart"]
    ordering = ["cart"]
    search_fields = ["cart"]


@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = ["product", "user", "priority", "timestamp"]
    list_filter = ["user", "priority", "timestamp"]
    ordering = ["timestamp", "user", "priority"]
    search_fields = ["priority", "user"]
