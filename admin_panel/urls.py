from django.urls import include, path
from rest_framework import routers

from admin_panel.swagger_views import DecoratedTokenRefreshView, DecoratedTokenObtainPairView
from admin_panel.views import UserViewSet, ClientEmployeeViewSet, ClientEmployeeTimeViewSet, CameraViewSet, \
    RunCameraView, ClientVisitStat

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'clients', ClientEmployeeViewSet)
router.register(r'cameras', CameraViewSet)
# router.register(r'employees', EmployeeViewSet)
router.register(r'employee_time', ClientEmployeeTimeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('cam_start_stop/', RunCameraView.as_view(), name='camera_start_stop'),
    path('client_visits/', ClientVisitStat.as_view(), name='client_visits'),
    path('login/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
]
