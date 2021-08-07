from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from app.admin_site import admin_site

#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('admin/', admin_site.urls),
    path('', include('app.urls')),
    #path('api/token/', TokenObtainPairView.as_view()),
    #path('api/token/refresh', TokenRefreshView.as_view()),
]