from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Passwords
from .serializers import PasswordSerializer, FullPasswordSerializer, PasswordListSerializer


class AddPasswordView(APIView):
    permission_classes = (IsAuthenticated,)

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

            # checking if the exact information are already in the database
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


class UpdatePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, id):
        serializer = PasswordSerializer(request.data)
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
            account_password = request.data['password']
            user_password = request.data['user_password']

            # checking user entered password
            if not user.check_password(user_password):
                response = {'detail': 'user password invalid!'}
                return Response(response)

            # checking if the password exist
            password = Passwords.objects.get(id=id)
            if not password:
                response = {'detail': 'password NOT found'}
                return Response(response)

            # checking if the exact information are already in the database
            is_exist = Passwords.objects.filter(
                user=user, site_name=site_name, site_url=site_url, username=username, email=email,
                password=account_password).exists()

            if is_exist:
                response = {'detail': 'The info is already saved!'}
                return Response(response)

            # setting new values for the Password
            password.site_name = site_name
            password.site_url = site_url
            password.username = username
            password.email = email
            password.password = account_password

            password.save()

            # return password data
            password_ser = FullPasswordSerializer(password)
            return Response(password_ser.data)

        return Response(serializer.errors)


class DeletePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        user = request.user

        if user.is_anonymous:
            raise AuthenticationFailed('unauthenticated!')

        # getting password from id we get in url
        password = Passwords.objects.filter(pk=pk, user_id=user.id).first()

        # checking if it exists
        if not password:
            response = {'detail': 'password NOT found!'}
            return Response(response)

        try:
            user_password = request.data['user_password']
        except Exception as e:
            # returning the error as a string in the response
            response = {'detail': str(e)}
            return Response(response)

        # checking user entered password
        if not user.check_password(user_password):
            response = {'detail': 'user password invalid!'}
            return Response(response)

        password.delete()

        response = {'detail': 'password deleted successfully!'}
        return Response(response)


class PasswordListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordListSerializer
    queryset = Passwords.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Passwords.objects.filter(user_id=user.id)


class ShowPasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = request.user

        if user.is_anonymous:
            raise AuthenticationFailed('unauthenticated!')

        # getting password from id we get in url
        password = Passwords.objects.get(pk=pk, user_id=user.id)

        # checking if it exists
        if not password:
            response = {'detail': 'password NOT found!'}
            return Response(response)

        try:
            user_password = request.data['user_password']
        except Exception as e:
            # returning the error as a string in the response
            response = {'detail': str(e)}
            return Response(response)

        # checking user entered password
        if not user.check_password(user_password):
            response = {'detail': 'user password invalid!'}
            return Response(response)

        serializer = FullPasswordSerializer(password)

        return Response(serializer.data)
