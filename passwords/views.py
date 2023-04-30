from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Passwords
from .serializers import PasswordSerializer, FullPasswordSerializer


class AddPasswordView(APIView):
    def post(self, request):
        # checking serializer validation
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user

            # check if we have the user and also if it is the authenticated user
            if not user:
                response = {'detail': 'user NOT found!'}
                return Response(response)
            if user.is_anonymous:
                raise AuthenticationFailed('unauthenticated!')

            site_name = request.data['site_name']
            site_url = request.data['site_url']
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            user_password = request.data['user_password']

            # checking user entered password
            if not user.check_password(user_password):
                response = {'detail': 'user password invalid!'}
                return Response(response)

            # checking if the exact informations are already in the database
            is_exist = Passwords.objects.filter(
                user=user, site_name=site_name, site_url=site_url, username=username, email=email,
                password=password).exists()

            if is_exist:
                response = {'detail': 'The info is already saved!'}
                return Response(response)

            # create new password
            try:
                new_password = Passwords.objects.create(
                    user=user, site_name=site_name, site_url=site_url, username=username, email=email,
                    password=password)
            except Exception as e:
                # returning the error as a string in the response
                response = {'detail': str(e)}
                return Response(response)

            # return password data
            password_ser = FullPasswordSerializer(new_password)
            return Response(password_ser.data)

        return Response(serializer.errors)
