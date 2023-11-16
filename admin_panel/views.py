from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import renderers
from rest_framework import filters as searchf
from rest_framework import permissions, parsers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from admin_panel.custom_viewsets import Custom_Viewsub, Client_Viewsub, Camera_Viewsub
from admin_panel.models import CustomUser, ClientEmployee, ClientEmployeeTime, Camera
from admin_panel.serializers import UserSerializer, ClientEmployeeSerializer, ClientEmployeeTimeSerializer, \
    CameraSerializer
from admin_panel.custom_permissions import IsAdminUser, IsSuperUser


# camera_list = [{'ip_address': '192.168.1.64', 'login': 'admin', 'password': 'softex2020', 'is_enter': True, 'real': 1}]
# my_app = Face_App(cameras=camera_list)
# my_app.run_function()


class UserViewSet(Custom_Viewsub):
    queryset = CustomUser.objects.order_by('-id')
    serializer_class = UserSerializer
    # filter_backends = [searchf.SearchFilter]
    # search_fields = ['title_uz']
    # pagination_class = CustomUserPagination
    permission_classes = [IsSuperUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)


class ClientEmployeeViewSet(Client_Viewsub):
    queryset = ClientEmployee.objects.order_by('id')
    serializer_class = ClientEmployeeSerializer
    search_fields = ['name']
    filter_backends = [DjangoFilterBackend, searchf.SearchFilter]
    filterset_fields = ['is_client', 'last_time']
    # pagination_class = CustomUserPagination
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)


class ClientEmployeeTimeViewSet(Client_Viewsub):
    queryset = ClientEmployeeTime.objects.order_by('id')
    serializer_class = ClientEmployeeTimeSerializer
    # search_fields = ['name']
    # filter_backends = [DjangoFilterBackend, searchf.SearchFilter]
    # filterset_fields = ['is_client']
    # pagination_class = CustomUserPagination
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)


class CameraViewSet(Camera_Viewsub):
    queryset = Camera.objects.order_by('id')
    serializer_class = CameraSerializer
    # search_fields = ['name']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_enter']
    # pagination_class = CustomUserPagination
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)
