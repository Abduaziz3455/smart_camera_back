from django.urls import include, path
from rest_framework import routers

from admin_panel.swagger_views import DecoratedTokenRefreshView, DecoratedTokenObtainPairView
from admin_panel.views import UserViewSet, ClientViewSet, CameraViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'cameras', CameraViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
]
