from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializers, LoginSerializer
from rest_framework.response import Response
from rest_framework import serializers, status
from django.conf import settings
from django.contrib import auth
import jwt
# Create your views here.


class RegisterView(GenericAPIView):
    serializer_class = UserSerializers

    def post(self, request):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)
        # print(settings.JWT_SECRET_KEY)
        if user:
            # print(settings.JWT_SECRET_KEY)
            auth_token = jwt.encode(
                {'username': user.username}, settings.JWT_SECRET_KEY, algorithm="HS256")
            # print(auth_token)
            serializer_class = UserSerializers(user)

            data = {'user': serializer_class.data, 'token': auth_token}
            return Response(data, status=status.HTTP_200_OK)
        # Send response
        return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
