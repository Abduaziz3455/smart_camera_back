from django.urls import include, path
from rest_framework import routers

from dev_panel.swagger_views import DecoratedTokenRefreshView, DecoratedTokenObtainPairView
from dev_panel.views import OrganizationViewSet

router = routers.DefaultRouter()
router.register(r'organizations', OrganizationViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
]
