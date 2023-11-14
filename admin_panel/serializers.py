from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from admin_panel.models import CustomUser, Client, Employee, EmployeeTime, Camera

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
        fields = ['id', 'username', 'password']


class ClientSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['image']:
            data['image'] = data['image'].replace(f"{BASE_URL}/media", "/media")
        if data['last_image']:
            data['last_image'] = data['last_image'].replace(f"{BASE_URL}/media", "/media")
        return data

    class Meta:
        model = Client
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['image']:
            data['image'] = data['image'].replace(f"{BASE_URL}/media", "/media")
        if data['last_image']:
            data['last_image'] = data['last_image'].replace(f"{BASE_URL}/media", "/media")

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeTime
        fields = '__all__'


class CameraSerializer(serializers.ModelSerializer):

    class Meta:
        model = Camera
        fields = '__all__'
