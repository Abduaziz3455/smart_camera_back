from datetime import datetime

from django.contrib.auth.models import update_last_login
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status, parsers, renderers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import (TokenBlacklistView, TokenObtainPairView, TokenRefreshView,
                                            TokenVerifyView, )


class TokenObtainPairResponseSerializer(TokenObtainPairSerializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        if not self.user.is_superuser:
            if self.user.organization.subscription_ends_date < datetime.today().date():
                raise exceptions.AuthenticationFailed(
                    "Organization date expired",
                    "organ_expired",
                )
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class DecoratedTokenObtainPairView(TokenObtainPairView):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)

    @swagger_auto_schema(responses=
                         {status.HTTP_200_OK: TokenObtainPairResponseSerializer, }
                         )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenRefreshView(TokenRefreshView):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)

    @swagger_auto_schema(responses=
                         {status.HTTP_200_OK: TokenRefreshResponseSerializer, }
                         )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(responses=
                         {status.HTTP_200_OK: TokenVerifyResponseSerializer, }
                         )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenBlacklistResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenBlacklistView(TokenBlacklistView):
    @swagger_auto_schema(responses=
                         {status.HTTP_200_OK: TokenBlacklistResponseSerializer, }
                         )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
