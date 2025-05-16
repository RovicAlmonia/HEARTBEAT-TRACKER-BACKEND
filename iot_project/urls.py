from django.contrib import admin
from django.urls import path
from heartbeat.views import (
    RegisterView, HeartbeatListCreate, 
    LogoutView, LogoutAllView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/logout-all/', LogoutAllView.as_view(), name='logout_all'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/heartbeat/', HeartbeatListCreate.as_view(), name='heartbeat'),
]
