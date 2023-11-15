from drf_yasg import renderers
from rest_framework import filters as searchf, status
from rest_framework import permissions, parsers
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from dev_panel.custom_viewsets import Organization_Viewsub
from dev_panel.models import Organization
from dev_panel.pagination import CustomPagination
from dev_panel.serializers import OrganizationSerializer


class OrganizationViewSet(Organization_Viewsub):
    queryset = Organization.objects.order_by('id')
    serializer_class = OrganizationSerializer
    search_fields = ['brand_name']
    filter_backends = [DjangoFilterBackend, searchf.SearchFilter]
    # filterset_fields = ['']
    # pagination_class = CustomUserPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)