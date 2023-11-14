from drf_yasg import renderers
from rest_framework import filters as searchf, status
from rest_framework import permissions, parsers
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from admin_panel.custom_viewsets import Custom_Viewsub, Client_Viewsub, Camera_Viewsub
from admin_panel.models import CustomUser, Client, Employee, EmployeeTime, Camera
from admin_panel.pagination import CustomPagination
from admin_panel.serializers import UserSerializer, ClientSerializer, EmployeeSerializer, CameraSerializer, EmployeeTimeSerializer

# camera_list = [{'ip_address': '192.168.1.64', 'login': 'admin', 'password': 'softex2020', 'is_enter': True, 'real': 1}]
# my_app = Face_App(cameras=camera_list)
# my_app.run_function()


class UserViewSet(Custom_Viewsub):
    queryset = CustomUser.objects.order_by('-id')
    serializer_class = UserSerializer
    # filter_backends = [searchf.SearchFilter]
    # search_fields = ['title_uz']
    # pagination_class = CustomUserPagination
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)


class ClientViewSet(Client_Viewsub):
    queryset = Client.objects.order_by('id')
    serializer_class = ClientSerializer
    search_fields = ['name']
    filter_backends = [DjangoFilterBackend, searchf.SearchFilter]
    filterset_fields = ['is_client', 'last_time']
    # pagination_class = CustomUserPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)


class EmployeeViewSet(Client_Viewsub):
    queryset = Employee.objects.order_by('id')
    serializer_class = EmployeeSerializer
    search_fields = ['name']
    filter_backends = [DjangoFilterBackend, searchf.SearchFilter]
    # pagination_class = CustomUserPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)


class EmployeeTimeViewSet(Client_Viewsub):
    queryset = EmployeeTime.objects.order_by('id')
    serializer_class = EmployeeTimeSerializer
    # search_fields = ['name']
    # filter_backends = [DjangoFilterBackend, searchf.SearchFilter]
    # filterset_fields = ['is_client']
    # pagination_class = CustomUserPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)
