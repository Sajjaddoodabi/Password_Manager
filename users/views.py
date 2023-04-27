from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from users.serializers import UserRegisterSerializer


class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

