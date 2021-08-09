from django.urls import path
from .views import (
    email_API_view,
    product_search_API_view,
    raw_sql_API_view,
    UserAPIView,
    UserDetailAPIView,
    CategoryAPIView,
    CategoryDetailAPIView,
    BrandAPIView,
    BrandDetailAPIView,
    ProductAPIView,
    ProductDetailAPIView,
    CartAPIView,
    CartDetailAPIView,
    CartItemAPIView,
    CartItemDetailAPIView,
    WatchAPIView,
    WatchDetailAPIView,
    PrescribePermissionAPIView,
    PrescribePermissionDetailAPIView
)


urlpatterns = [
    path('api/users_api_view/<str:serializer_data>/', UserAPIView.as_view(), name="UserAPIView"),
    path('api/users_detail_api_view/<str:serializer_data>/', UserDetailAPIView.as_view(), name="UserDetailAPIView"),
    path('api/categories_api_view/<str:serializer_data>/', CategoryAPIView.as_view(), name="CategoryAPIView"),
    path('api/categories_detail_api_view/<str:serializer_data>/', CategoryDetailAPIView.as_view(), name="CategoryDetailAPIView"),
    path('api/brands_api_view/<str:serializer_data>/', BrandAPIView.as_view(), name="BrandAPIView"),
    path('api/brands_detail_api_view/<str:serializer_data>/', BrandDetailAPIView.as_view(), name="BrandDetailAPIView"),
    path('api/products_api_view/<str:serializer_data>/', ProductAPIView.as_view(), name="ProductAPIView"),
    path('api/products_detail_api_view/<str:serializer_data>/', ProductDetailAPIView.as_view(), name="ProductDetailAPIView"),
    path('api/carts_api_view/<str:serializer_data>/', CartAPIView.as_view(), name="CartAPIView"),
    path('api/carts_detail_api_view/<str:serializer_data>/', CartDetailAPIView.as_view(), name="CartDetailAPIView"),
    path('api/prescribe_permission_api_view/<str:serializer_data>/', PrescribePermissionAPIView.as_view(), name="PrescribePermissionAPIView"),
    path('api/prescribe_permission_detail_api_view/<str:serializer_data>/', PrescribePermissionDetailAPIView.as_view(), name="PrescribePermissionDetailAPIView"),
    path('api/watches_api_view/<str:serializer_data>/', WatchAPIView.as_view(), name="WatchAPIView"),
    path('api/watches_detail_api_view/<str:serializer_data>/', WatchDetailAPIView.as_view(), name="WatchDetailAPIView"),
    path('api/cart_items_api_view/<str:serializer_data>/', CartItemAPIView.as_view(), name="CartItemAPIView"),
    path('api/cart_items_detail_api_view/<str:serializer_data>/', CartItemDetailAPIView.as_view(), name="CartItemDetailAPIView"),
    path('api/email/', email_API_view, name="EmailAPIView"),
    path('api/search/<str:search_string>/', product_search_API_view, name="SearchActionAPIView"),
    path('api/raw_sql/', raw_sql_API_view, name="RawSQLAPIView")
]