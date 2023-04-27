from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from users.serializers import UserRegisterSerializer, UserSerializer


class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


class UserView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        return AuthenticationFailed('Unauthenticated!')
