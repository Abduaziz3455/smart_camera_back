from datetime import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from admin_panel.models import CustomUser, ClientEmployee, ClientEmployeeTime, Camera

BASE_URL = ''
if settings.DEBUG:
    BASE_URL = settings.SITE_URL
else:
    BASE_URL = settings.LOCAL


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).update(instance, validated_data)

    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'username', 'password', 'organization', 'is_active', 'is_staff', 'is_superuser',
                  'date_joined', 'last_login', 'avatar', 'user_permissions']


class ClientEmployeeSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['image']:
            data['image'] = data['image'].replace(f"{BASE_URL}/media", "/media")
        if data['last_image']:
            data['last_image'] = data['last_image'].replace(f"{BASE_URL}/media", "/media")
        return data

    class Meta:
        model = ClientEmployee
        fields = '__all__'


class ClientEmployeeTimeSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['employee_name'] = ClientEmployee.objects.get(id=data['employee']).name
        return data

    class Meta:
        model = ClientEmployeeTime
        fields = '__all__'


class CameraSerializer(serializers.ModelSerializer):

    class Meta:
        model = Camera
        fields = '__all__'


class ClientStat_Serial(serializers.Serializer):
    time = serializers.DateTimeField()
    first_visit = serializers.IntegerField()
    re_visit = serializers.IntegerField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        date = self.context.get('date', None)
        if date:
            if date == 'month':
                data['time'] = datetime.strptime(data['time'], "%d.%m.%Y %H:%M").date().month
            else:
                data['time'] = datetime.strptime(data['time'], "%d.%m.%Y %H:%M").date().day
        return data

    class Meta:
        model = ClientEmployee
        fields = "__all__"
