from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User

from users.serializers import UserRegisterSerializer, UserSerializer, ChangePasswordSerializer, ResetPasswordSerializer


class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


class ActiveUserView(UpdateAPIView):
    # todo
    pass


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: HttpRequest):
        user = request.user
        if not user.is_authenticated:
            raise AuthenticationFailed('unauthenticated!')

        serializer = UserSerializer(user)
        return Response(serializer.data)


class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()

    def get_object(self):

        # returning the authenticated user
        if self.request.user.is_authenticated:
            return self.request.user
        return AuthenticationFailed('Unauthenticated!')

    def update(self, request, *args, **kwargs):
        # get authenticated user
        user = self.get_object()

        try:
            # get serializer data
            current_password = request.data['current_password']
            new_password = request.data['new_password']
            confirm_password = request.data['confirm_password']

        except Exception as e:
            # return any possible errors
            response = {'detail': str(e)}
            return Response(response)

        # check if user entered correct password
        if user.check_password(current_password):
            # check if the new pass is not the exact current one
            if new_password != current_password:
                if new_password == confirm_password:
                    user.password = make_password(new_password)
                    user.save()

                    response = {'detail': 'password changed successfully!!'}
                    return Response(response)

                else:
                    response = {'detail': 'password and confirm password does NOT match!!'}
                    return Response(response)
            else:
                response = {'detail': 'You cant user your current password as the new one'}
                return Response(response)
        else:
            response = {'detail': 'password is Incorrect!'}
            return Response(response)


class UpdateUserView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        # returning the authenticated user
        if self.request.user.is_authenticated:
            return self.request.user
        return AuthenticationFailed('Unauthenticated!')


class ResetPasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResetPasswordSerializer
    queryset = User.objects.all()

    def get_object(self):
        # returning the authenticated user
        if self.request.user.is_authenticated:
            return self.request.user
        return AuthenticationFailed('Unauthenticated!')

    # todo
