from django.conf import settings
# from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from dev_panel.models import Organization

BASE_URL = ''
if settings.DEBUG:
    BASE_URL = settings.SITE_URL
else:
    BASE_URL = settings.LOCAL


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__'  