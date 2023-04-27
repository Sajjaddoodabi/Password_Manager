from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


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

        # set password for user
        user.set_password(validated_data.get('password'))

        # save user into database
        user.save()

        return user
