from random import randint

from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active')
        read_only_fields = ('id', 'is_active')


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate(self, attrs):
        # check if password is strong enough
        validate_password(attrs.get('password'))

        # checking if password and confirm password are the same
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError(_('password and confirm password does NOT match!'))

        return attrs

    @staticmethod
    def clean_validated_data(validated_data):
        # deleting confirm password because we dont need it anymore
        validated_data.pop('confirm_password')

        return validated_data

    def create(self, validated_data):
        # create user with given data
        user = self.Meta.model.objects.create(**self.clean_validated_data(validated_data))

        # generate an active code for the user and set user activation to False
        user.email_active_code = randint(100000, 1000000)
        user.is_active = False

        # set password for user
        user.set_password(validated_data.get('password'))

        # save user into database
        user.save()

        send_mail = {

        }

        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('current_password', 'new_password', 'confirm_password')

    def validate(self, attrs):
        # check if password is strong enough
        validate_password(attrs.get('new_password'))

        # checking if password and confirm password are the same
        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise serializers.ValidationError(_('password and confirm password does NOT match!'))

        return attrs


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('password', 'confirm_password')

    def validate(self, attrs):
        # check if password is strong enough
        validate_password(attrs.get('password'))

        # checking if password and confirm password are the same
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError(_('password and confirm password does NOT match!'))

        return attrs
