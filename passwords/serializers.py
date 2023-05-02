from rest_framework import serializers

from passwords.models import Passwords


class FullPasswordSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Passwords
        fields = (
            'id', 'user', 'site_name', 'site_url', 'username', 'email', 'password', 'date_created', 'last_date_edited')
        read_only_fields = ('id', 'date_created', 'last_date_edited')


class PasswordSerializer(serializers.ModelSerializer):
    user_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = Passwords
        fields = ('id', 'site_name', 'site_url', 'username', 'email', 'password', 'user_password')
