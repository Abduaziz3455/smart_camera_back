from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="SMART CAM",
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    url=f"{settings.SITE_URL}"
)

urlpatterns = [
                  path('my-special-admin-login/', admin.site.urls),
                  re_path(r'^$', schema_view.with_ui(
                      'swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('', include('admin_panel.urls')),
                  re_path(r'^media/(?P<path>.*)$', serve,
                          {'document_root': settings.MEDIA_ROOT}),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATICFILES_DIRS)
else:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
