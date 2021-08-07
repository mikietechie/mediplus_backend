from django.urls import path
from .views import (
    email_API_view,
    UserAPIView,
    UserDetailAPIView,
    product_search_API_view,
    raw_sql_API_view
)


urlpatterns = [
    path('api/users_api_view/<str:serializer_data>/', UserAPIView.as_view(), name="GenericAPIView"),
    path('api/users_detail_api_view/<str:serializer_data>/', UserDetailAPIView.as_view(), name="GenericDetailAPIView"),
    path('api/email/', email_API_view, name="EmailAPIView"),
    path('api/search/<str:search_string>/', product_search_API_view, name="SearchActionAPIView"),
    path('api/raw_sql/', raw_sql_API_view, name="RawSQLAPIView")
]