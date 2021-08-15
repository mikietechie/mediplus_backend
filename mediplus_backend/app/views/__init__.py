from .rest_views import (
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
from .http_views import (
    index_view,
    login_view,
    register_view,
    logout_view
)