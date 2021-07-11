from django.contrib.auth import authenticate
from django.forms import PasswordInput
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from panel.validators import validate_mail, is_email_valid

from panel.models import MyUser


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}
                                     , write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Incorrect username or password.')
        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')
        return user


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}
                                     , write_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField()
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    #
    def validate(self, attrs):
        if attrs.get('username'):
            if attrs.get('phone'):
                if attrs.get('email') and not is_email_valid(email=attrs.get('email')):
                    raise ValidationError('Invalid Email')
                if not attrs.get('phone').replace('+', '00').isnumeric():
                    raise ValidationError('wrong phone number')
                return attrs
        else:
            return attrs

    def create(self, validated_data):
        return MyUser.objects.create_user(username=validated_data.pop('username'),
                                          password=validated_data.pop('password'),
                                          **validated_data)
