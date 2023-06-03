from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from . import serializers
from rest_framework import status, generics
from rest_framework.views import APIView
from . import permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data.copy()
        data.update({"token": token.key})
        return Response(data, status.HTTP_201_CREATED, headers)


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data.copy()
        data.update({"token": token.key})
        return Response(data, status.HTTP_202_ACCEPTED)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        Token.objects.get(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)


class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = serializers.UserSerializer(request.user)
        data = serializer.data.copy()
        data.update({"token": Token.objects.get(user=request.user).key})
        return Response(data, status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        Token.objects.get(user=request.user).delete()
        request.user.delete()
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.check_password(request.data["password"]):
            if "new_password" in request.data:
                user.set_password(request.data["new_password"])
            serializer = serializers.UserSerializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = dict(serializer.data).copy()
            data.update({"token": Token.objects.get(user=user).key})
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
