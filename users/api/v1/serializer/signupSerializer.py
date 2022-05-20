from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from ....models import User

import re

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)

    def validate(self, data):
        error = {}
        if not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,25}$',data['password']):
            error['password'] = "Password didn't match minimum requirement."
        if not data['password'] == data['confirm_password']:
            error['confirm_password'] = "Passwords didn't match."
        if User.objects.filter(email=data['email']).exists():
            error['email'] = "User with this email exists."
        if error:
            raise serializers.ValidationError(error)

        data.pop('confirm_password')
        return data

    def create(self, validated_data):
        email = validated_data.pop('email')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        password = validated_data.pop('password')

        user = User.objects.create_user(email=email, password=password,
                                        **{"first_name": first_name, "last_name": last_name})

        return user
