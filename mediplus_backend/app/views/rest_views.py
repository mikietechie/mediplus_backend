from app.models import (
    User,
    Brand,
    Category,
    Product,
    Cart,
    CartItem,
    Watch,
    PrescribePermission
)
from app.serializers import (
    UserSerializer,
    BrandSerializer,
    CategorySerializer,
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    WatchSerializer,
    PrescribePermissionSerializer
)
from app.utilities import (
    clean_filters,
    dict_fetch_all,
    get_and_pop_from_dict,
    get_attr_or_none
)
from app import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
from rest_framework.parsers import JSONParser

from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json


#   User model views
class UserAPIView(APIView):
    
    def get(self, request, serializer_data):
        filters = clean_filters(request.GET)
        if get_and_pop_from_dict(filters, "paginate"):
            page = get_and_pop_from_dict(filters, "page")
            per_page = get_and_pop_from_dict(filters, "per_page") or 10
            query_set = User.objects.filter(**filters)
            paginator = Paginator(query_set, per_page=per_page)
            page = paginator.get_page(page)
            return Response(ReturnDict({
                        "users": [getattr(UserSerializer(instance), f"{serializer_data}") for instance in page.object_list],
                        "count": paginator.count,
                        "num_pages": paginator.num_pages,
                        "number": page.number,
                        "has_next": page.has_next(),
                        "has_previous": page.has_previous(),
                        "has_other_pages": page.has_other_pages(),
                        "next_page_index": get_attr_or_none(page, "next_page_number", is_func=True),
                        "previous_page_index": get_attr_or_none(page, "previous_page_number", is_func=True),
                        "page_range": list(paginator.page_range)
                    },
                    serializer=UserSerializer
                ),
                status=status.HTTP_200_OK
            )
        users = User.objects.filter(**filters)
        return Response(
            ReturnList([getattr(UserSerializer(user), f"{serializer_data}") for user in users], serializer=UserSerializer),
            status=status.HTTP_200_OK
        )
    
    def post(self, request, serializer_data):
        serialized_user =  UserSerializer(data=request.data)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(getattr(serialized_user, serializer_data), status=status.HTTP_201_CREATED)
        return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserDetailAPIView(APIView):

    def get_user(self, filters):
        try:
            return User.objects.get(**clean_filters(filters))
        except:
            raise Http404("Not found")

    def get(self, request, serializer_data):
        user = self.get_user(request.GET)
        serialized_user = UserSerializer(user)
        return Response(getattr(serialized_user, f"{serializer_data}"), status=status.HTTP_200_OK)

    def put(self, request, serializer_data):
        user = self.get_user(request.GET)
        serialized_user = UserSerializer(user, data=request.data)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(getattr(serialized_user, serializer_data), status=status.HTTP_202_ACCEPTED)
        return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, serializer_data):
        user = self.get_user(request.GET)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#   Category model views
class CategoryAPIView(APIView):
    
    def get(self, request, serializer_data):
        filters = clean_filters(request.GET)
        categories = Category.objects.filter(**filters)
        return Response(
            ReturnList([getattr(CategorySerializer(category), f"{serializer_data}") for category in categories], serializer=CategorySerializer),
            status=status.HTTP_200_OK
        )
    
    def post(self, request, serializer_data):
        serialized_category =  CategorySerializer(data=request.data)
        if serialized_category.is_valid():
            serialized_category.save()
            return Response(getattr(serialized_category, serializer_data), status=status.HTTP_201_CREATED)
        return Response(serialized_category.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CategoryDetailAPIView(APIView):

    def get_category(self, filters):
        try:
            return Category.objects.get(**clean_filters(filters))
        except:
            raise Http404("Not found")

    def get(self, request, serializer_data):
        category = self.get_category(request.GET)
        serialized_category = CategorySerializer(category)
        return Response(getattr(serialized_category, f"{serializer_data}"), status=status.HTTP_200_OK)

    def put(self, request, serializer_data):
        category = self.get_category(request.GET)
        serialized_category = CategorySerializer(category, data=request.data)
        if serialized_category.is_valid():
            serialized_category.save()
            return Response(getattr(serialized_category, serializer_data), status=status.HTTP_202_ACCEPTED)
        return Response(serialized_category.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, serializer_data):
        category = self.get_category(request.GET)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#   Brand model views
class BrandAPIView(APIView):
    
    def get(self, request, serializer_data):
        filters = clean_filters(request.GET)
        brands = Brand.objects.filter(**filters)
        return Response(
            ReturnList([getattr(BrandSerializer(brand), f"{serializer_data}") for brand in brands], serializer=BrandSerializer),
            status=status.HTTP_200_OK
        )
    
    def post(self, request, serializer_data):
        serialized_brand =  BrandSerializer(data=request.data)
        if serialized_brand.is_valid():
            serialized_brand.save()
            return Response(getattr(serialized_brand, serializer_data), status=status.HTTP_201_CREATED)
        return Response(serialized_brand.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BrandDetailAPIView(APIView):

    def get_brand(self, filters):
        try:
            return Brand.objects.get(**clean_filters(filters))
        except:
            raise Http404("Not found")

    def get(self, request, serializer_data):
        brand = self.get_brand(request.GET)
        serialized_brand = BrandSerializer(brand)
        return Response(getattr(serialized_brand, f"{serializer_data}"), status=status.HTTP_200_OK)

    def put(self, request, serializer_data):
        brand = self.get_brand(request.GET)
        serialized_brand = BrandSerializer(brand, data=request.data)
        if serialized_brand.is_valid():
            serialized_brand.save()
            return Response(getattr(serialized_brand, serializer_data), status=status.HTTP_202_ACCEPTED)
        return Response(serialized_brand.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, serializer_data):
        brand = self.get_brand(request.GET)
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#   Product model views
class ProductAPIView(APIView):
    
    def get(self, request, serializer_data):
        filters = clean_filters(request.GET)
        if get_and_pop_from_dict(filters, "paginate"):
            page = get_and_pop_from_dict(filters, "page")
            per_page = get_and_pop_from_dict(filters, "per_page") or 10
            query_set = Product.objects.filter(**filters)
            paginator = Paginator(query_set, per_page=per_page)
            page = paginator.get_page(page)
            return Response(ReturnDict({
                        "products": [getattr(ProductSerializer(instance), f"{serializer_data}") for instance in page.object_list],
                        "count": paginator.count,
                        "num_pages": paginator.num_pages,
                        "number": page.number,
                        "has_next": page.has_next(),
                        "has_previous": page.has_previous(),
                        "has_other_pages": page.has_other_pages(),
                        "next_page_index": get_attr_or_none(page, "next_page_number", is_func=True),
                        "previous_page_index": get_attr_or_none(page, "previous_page_number", is_func=True),
                        "page_range": list(paginator.page_range)
                    },
                    serializer=ProductSerializer
                ),
                status=status.HTTP_200_OK
            )
        products = Product.objects.filter(**filters)
        return Response(
            ReturnList([getattr(ProductSerializer(product), f"{serializer_data}") for product in products], serializer=ProductSerializer),
            status=status.HTTP_200_OK
        )
    
    def post(self, request, serializer_data):
        serialized_product =  ProductSerializer(data=request.data)
        if serialized_product.is_valid():
            serialized_product.save()
            return Response(getattr(serialized_product, serializer_data), status=status.HTTP_201_CREATED)
        return Response(serialized_product.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductDetailAPIView(APIView):

    def get_product(self, filters):
        try:
            return Product.objects.get(**clean_filters(filters))
        except:
            raise Http404("Not found")

    def get(self, request, serializer_data):
        product = self.get_product(request.GET)
        serialized_product = ProductSerializer(product)
        return Response(getattr(serialized_product, f"{serializer_data}"), status=status.HTTP_200_OK)

    def put(self, request, serializer_data):
        product = self.get_product(request.GET)
        serialized_product = ProductSerializer(product, data=request.data)
        if serialized_product.is_valid():
            serialized_product.save()
            return Response(getattr(serialized_product, serializer_data), status=status.HTTP_202_ACCEPTED)
        return Response(serialized_product.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, serializer_data):
        product = self.get_product(request.GET)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#   Cart model views
class CartAPIView(APIView):
    
    def get(self, request, serializer_data):
        filters = clean_filters(request.GET)
        if get_and_pop_from_dict(filters, "paginate"):
            page = get_and_pop_from_dict(filters, "page")
            per_page = get_and_pop_from_dict(filters, "per_page") or 10
            query_set = Cart.objects.filter(**filters)
            paginator = Paginator(query_set, per_page=per_page)
            page = paginator.get_page(page)
            return Response(ReturnDict({
                        "carts": [getattr(CartSerializer(instance), f"{serializer_data}") for instance in page.object_list],
                        "count": paginator.count,
                        "num_pages": paginator.num_pages,
                        "number": page.number,
                        "has_next": page.has_next(),
                        "has_previous": page.has_previous(),
                        "has_other_pages": page.has_other_pages(),
                        "next_page_index": get_attr_or_none(page, "next_page_number", is_func=True),
                        "previous_page_index": get_attr_or_none(page, "previous_page_number", is_func=True),
                        "page_range": list(paginator.page_range)
                    },
                    serializer=CartSerializer
                ),
                status=status.HTTP_200_OK
            )
        carts = Cart.objects.filter(**filters)
        return Response(
            ReturnList([getattr(CartSerializer(cart), f"{serializer_data}") for cart in carts], serializer=CartSerializer),
            status=status.HTTP_200_OK
        )
    
    def post(self, request, serializer_data):
        serialized_cart =  CartSerializer(data=request.data)
        if serialized_cart.is_valid():
            serialized_cart.save()
            return Response(getattr(serialized_cart, serializer_data), status=status.HTTP_201_CREATED)
        return Response(serialized_cart.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CartDetailAPIView(APIView):

    def get_cart(self, filters):
        try:
            return Cart.objects.get(**clean_filters(filters))
        except:
            raise Http404("Not found")

    def get(self, request, serializer_data):
        cart = self.get_cart(request.GET)
        serialized_cart = CartSerializer(cart)
        return Response(getattr(serialized_cart, f"{serializer_data}"), status=status.HTTP_200_OK)

    def put(self, request, serializer_data):
        cart = self.get_cart(request.GET)
        serialized_cart = CartSerializer(cart, data=request.data)
        if serialized_cart.is_valid():
            serialized_cart.save()
            return Response(getattr(serialized_cart, serializer_data), status=status.HTTP_202_ACCEPTED)
        return Response(serialized_cart.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, serializer_data):
        cart = self.get_cart(request.GET)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#   CartItem model views
class CartItemAPIView(APIView):
    
    def get(self, request, serializer_data):
        filters = clean_filters(request.GET)
        if get_and_pop_from_dict(filters, "paginate"):
            page = get_and_pop_from_dict(filters, "page")
            per_page = get_and_pop_from_dict(filters, "per_page") or 10
            query_set = CartItem.objects.filter(**filters)
            paginator = Paginator(query_set, per_page=per_page)
            page = paginator.get_page(page)
            return Response(ReturnDict({
                        "cart_items": [getattr(CartItemSerializer(instance), f"{serializer_data}") for instance in page.object_list],
                        "count": paginator.count,
                        "num_pages": paginator.num_pages,
                        "number": page.number,
                        "has_next": page.has_next(),
                        "has_previous": page.has_previous(),
                        "has_other_pages": page.has_other_pages(),
                        "next_page_index": get_attr_or_none(page, "next_page_number", is_func=True),
                        "previous_page_index": get_attr_or_none(page, "previous_page_number", is_func=True),
                        "page_range": list(paginator.page_range)
                    },
                    serializer=CartItemSerializer
                ),
                status=status.HTTP_200_OK
            )
        cart_items = CartItem.objects.filter(**filters)
        return Response(
            ReturnList([getattr(CartItemSerializer(cart_item), f"{serializer_data}") for cart_item in cart_items], serializer=CartItemSerializer),
            status=status.HTTP_200_OK
        )
    
    def post(self, request, serializer_data):
        serialized_cart_item =  CartItemSerializer(data=request.data)
        if serialized_cart_item.is_valid():
            serialized_cart_item.save()
            return Response(getattr(serialized_cart_item, serializer_data), status=status.HTTP_201_CREATED)
        print(serialized_cart_item.errors)
        return Response(serialized_cart_item.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CartItemDetailAPIView(APIView):

    def get_cart_item(self, filters):
        try:
            return CartItem.objects.get(**clean_filters(filters))
        except:
            raise Http404("Not found")

    def get(self, request, serializer_data):
        cart_item = self.get_cart_item(request.GET)
        serialized_cart_item = CartItemSerializer(cart_item)
        return Response(getattr(serialized_cart_item, f"{serializer_data}"), status=status.HTTP_200_OK)

    def put(self, request, serializer_data):
        cart_item = self.get_cart_item(request.GET)
        serialized_cart_item = CartItemSerializer(cart_item, data=request.data)
        if serialized_cart_item.is_valid():
            serialized_cart_item.save()
            return Response(getattr(serialized_cart_item, serializer_data), status=status.HTTP_202_ACCEPTED)
        return Response(serialized_cart_item.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, serializer_data):
        cart_item = self.get_cart_item(request.GET)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#   Watch model views
class WatchAPIView(APIView):
    
    def get(self, request, serializer_data):
        filters = clean_filters(request.GET)
        if get_and_pop_from_dict(filters, "paginate"):
            page = get_and_pop_from_dict(filters, "page")
            per_page = get_and_pop_from_dict(filters, "per_page") or 10
            query_set = Watch.objects.filter(**filters)
            paginator = Paginator(query_set, per_page=per_page)
            page = paginator.get_page(page)
            return Response(ReturnDict({
                        "watches": [getattr(WatchSerializer(instance), f"{serializer_data}") for instance in page.object_list],
                        "count": paginator.count,
                        "num_pages": paginator.num_pages,
                        "number": page.number,
                        "has_next": page.has_next(),
                        "has_previous": page.has_previous(),
                        "has_other_pages": page.has_other_pages(),
                        "next_page_index": get_attr_or_none(page, "next_page_number", is_func=True),
                        "previous_page_index": get_attr_or_none(page, "previous_page_number", is_func=True),
                        "page_range": list(paginator.page_range)
                    },
                    serializer=WatchSerializer
                ),
                status=status.HTTP_200_OK
            )
        watches = Watch.objects.filter(**filters)
        return Response(
            ReturnList([getattr(WatchSerializer(watch), f"{serializer_data}") for watch in watches], serializer=WatchSerializer),
            status=status.HTTP_200_OK
        )
    
    def post(self, request, serializer_data):
        serialized_watch =  WatchSerializer(data=request.data)
        if serialized_watch.is_valid():
            serialized_watch.save()
            return Response(getattr(serialized_watch, serializer_data), status=status.HTTP_201_CREATED)
        return Response(serialized_watch.errors, status=status.HTTP_400_BAD_REQUEST)
    

class WatchDetailAPIView(APIView):

    def get_watch(self, filters):
        try:
            return Watch.objects.get(**clean_filters(filters))
        except:
            raise Http404("Not found")

    def get(self, request, serializer_data):
        watch = self.get_watch(request.GET)
        serialized_watch = WatchSerializer(watch)
        return Response(getattr(serialized_watch, f"{serializer_data}"), status=status.HTTP_200_OK)

    def put(self, request, serializer_data):
        watch = self.get_watch(request.GET)
        serialized_watch = WatchSerializer(watch, data=request.data)
        if serialized_watch.is_valid():
            serialized_watch.save()
            return Response(getattr(serialized_watch, serializer_data), status=status.HTTP_202_ACCEPTED)
        return Response(serialized_watch.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, serializer_data):
        watch = self.get_watch(request.GET)
        watch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#   PrescribePermission model views
class PrescribePermissionAPIView(APIView):
    
    def get(self, request, serializer_data):
        filters = clean_filters(request.GET)
        if get_and_pop_from_dict(filters, "paginate"):
            page = get_and_pop_from_dict(filters, "page")
            per_page = get_and_pop_from_dict(filters, "per_page") or 10
            query_set = PrescribePermission.objects.filter(**filters)
            paginator = Paginator(query_set, per_page=per_page)
            page = paginator.get_page(page)
            return Response(ReturnDict({
                        "prescribe_permissions": [getattr(PrescribePermissionSerializer(instance), f"{serializer_data}") for instance in page.object_list],
                        "count": paginator.count,
                        "num_pages": paginator.num_pages,
                        "number": page.number,
                        "has_next": page.has_next(),
                        "has_previous": page.has_previous(),
                        "has_other_pages": page.has_other_pages(),
                        "next_page_index": get_attr_or_none(page, "next_page_number", is_func=True),
                        "previous_page_index": get_attr_or_none(page, "previous_page_number", is_func=True),
                        "page_range": list(paginator.page_range)
                    },
                    serializer=PrescribePermissionSerializer
                ),
                status=status.HTTP_200_OK
            )
        prescribe_permissions = PrescribePermission.objects.filter(**filters)
        return Response(
            ReturnList([getattr(PrescribePermissionSerializer(prescribe_permission), f"{serializer_data}") for prescribe_permission in prescribe_permissions], serializer=PrescribePermissionSerializer),
            status=status.HTTP_200_OK
        )
    
    def post(self, request, serializer_data):
        serialized_prescribe_permission =  PrescribePermissionSerializer(data=request.data)
        if serialized_prescribe_permission.is_valid():
            serialized_prescribe_permission.save()
            return Response(getattr(serialized_prescribe_permission, serializer_data), status=status.HTTP_201_CREATED)
        return Response(serialized_prescribe_permission.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PrescribePermissionDetailAPIView(APIView):

    def get_prescribe_permission(self, filters):
        try:
            return PrescribePermission.objects.get(**clean_filters(filters))
        except:
            raise Http404("Not found")

    def get(self, request, serializer_data):
        prescribe_permission = self.get_prescribe_permission(request.GET)
        serialized_prescribe_permission = PrescribePermissionSerializer(prescribe_permission)
        return Response(getattr(serialized_prescribe_permission, f"{serializer_data}"), status=status.HTTP_200_OK)

    def put(self, request, serializer_data):
        prescribe_permission = self.get_prescribe_permission(request.GET)
        serialized_prescribe_permission = PrescribePermissionSerializer(prescribe_permission, data=request.data)
        if serialized_prescribe_permission.is_valid():
            serialized_prescribe_permission.save()
            return Response(getattr(serialized_prescribe_permission, serializer_data), status=status.HTTP_202_ACCEPTED)
        return Response(serialized_prescribe_permission.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, serializer_data):
        prescribe_permission = self.get_prescribe_permission(request.GET)
        prescribe_permission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def product_search_API_view(request, search_string):
    products = Product.objects.filter(Q(name__icontains = '{search_string}') | Q(description__icontains = '{search_string}'))
    serialized_products = ProductSerializer(products, many=True)
    return Response(
            serialized_products,
            status=status.HTTP_200_OK
        )


@csrf_exempt
@api_view(["POST"])
def email_API_view(request):
    data = request.data
    subject = data.get("subject")
    message = data.get("message")
    from_email = data.get("from_email")
    to_email = data.get("to_email")
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=(to_email, ),
            fail_silently=False,
        )
        return Response(
            ReturnDict(
                {"message": "Thank you your email has been sent!"},
                serializer = serializers.Serializer
            ),
            status = status.HTTP_202_ACCEPTED
        )
    except:
        return Response(
            ReturnDict(
                {"message": "Sorry something went wrong!"},
                serializer = serializers.Serializer
            ),
            status = status.HTTP_400_BAD_REQUEST
        )

@csrf_exempt
@api_view(["POST"])
def raw_sql_API_view(request):
    raw_sql = request.data.get("raw_sql")
    if "drop" in raw_sql.lower():
        return Response(status=status.HTTP_403_FORBIDDEN)
    with connection.cursor() as cursor:
        query_result = {"sql": raw_sql}
        try:
            cursor.execute(raw_sql)
            if "select" not in raw_sql.lower():
                query_result.update({})
            else:
                query_result.update({
                    "columns": [col[0] for col in cursor.description],
                    "rows": cursor.fetchall()
                })
            return Response(
                ReturnDict(
                    query_result,
                    serializer = serializers.Serializer
                ),
                status = status.HTTP_200_OK
            )     
        except:
            return Response(status = status.HTTP_400_BAD_REQUEST)


####    CSRF exempted delete api views to be removed when i find out how to do fetch delete requests

@csrf_exempt
def watch_delete_api(request):
    try:
        watch = Watch.objects.get(**clean_filters(request.GET))
        watch.delete()
        return JsonResponse({"message": "Watch deleted successfully!"})
    except Watch.DoesNotExist:
        return JsonResponse({"message": "Does not exist!"}, status=status.HTTP_404_NOT_FOUND)