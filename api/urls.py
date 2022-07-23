from django.urls import include, path
from rest_framework import routers
from django.urls import path
from api import views

from rest_framework_simplejwt import views as jwt_views


router = routers.DefaultRouter()
router.register(r'register', views.CreateUserAPIView, basename='MyModel')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
