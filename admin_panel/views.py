import threading

from django.db.models import Count, Q
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import renderers
from rest_framework import filters as searchf
from rest_framework import permissions, parsers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from admin_panel.custom_permissions import IsAdminUser, IsSuperUser, IsExpired
from admin_panel.custom_viewsets import Custom_Viewsub, Client_Viewsub, Camera_Viewsub
from admin_panel.models import CustomUser, ClientEmployee, ClientEmployeeTime, Camera
from admin_panel.serializers import UserSerializer, ClientEmployeeSerializer, ClientEmployeeTimeSerializer, \
    CameraSerializer, ClientStat_Serial
from smart_cam.main_video import Face_App

camera_list = [{'ip_address': '192.168.1.64', 'login': 'admin', 'password': 'softex2020', 'is_enter': True, 'real': 1}]


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
    permission_classes = [IsAdminUser, IsExpired]
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
    permission_classes = [IsAdminUser, IsExpired]
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
    permission_classes = [IsAdminUser, IsExpired]
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)


class RunCameraView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):

        global my_app

        if 'my_app' not in globals():
            my_app = Face_App(cameras=camera_list)
            camera = threading.Thread(target=my_app.run_function)
            camera.start()
            return JsonResponse({'data': 'Muvaffaqiyatli start berildi!'})
        else:
            my_app.stop()
            del globals()['my_app']
            return JsonResponse({'data': 'Muvaffaqiyatli stop qilindi!'})


class ClientVisitStat(GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ClientEmployee.objects.order_by('id')
    serializer_class = ClientEmployeeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_client', 'last_time']

    def get(self, request):
        daily_stats = self.get_queryset().annotate(time=TruncDay('created_time')) \
            .annotate(first_visit=Count('id', filter=Q(enter_count=1))) \
            .annotate(re_visit=Count('id', filter=Q(enter_count__gt=1))). \
            filter(status=True, is_client=True)

        # if start_date:
        #     start_date = datetime.strptime(start_date, "%m.%Y").date()
        #     daily_stats = daily_stats.filter(
        #         Q(created_date__month=start_date.month) & Q(created_date__year=start_date.year))

        context = {'date': 'day'}
        serializer = ClientStat_Serial(daily_stats.order_by('-created_time'), many=True, context=context)
        dicts = serializer.data
        #
        cum_list = []
        for dictionary in dicts:
            time = dictionary['time']
            order_completed = dictionary['first_visit']
            order_rejected = dictionary['re_visit']
            found = False
            for one_dict in cum_list:
                if one_dict['time'] == time:
                    one_dict['first_visit'] += order_completed
                    one_dict['re_visit'] += order_rejected
                    found = True
                    break

            if not found:
                cumulative_sums = {
                    'time': time,
                    'first_visit': order_completed,
                    're_visit': order_rejected
                }
                cum_list.append(cumulative_sums)
        times = []
        for i in cum_list:
            time = i['time']
            times.append(time)
        for i in range(1, 32):
            if i in times:
                continue
            else:
                cumulative_sums = {
                    'time': i,
                    'first_visit': 0,
                    're_visit': 0
                }
                cum_list.append(cumulative_sums)
        cum_list = sorted(cum_list, key=lambda x: x["time"])

        return Response(cum_list)
