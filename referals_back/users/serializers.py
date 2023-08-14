from .models import Referal, SmsCode, User
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'email', 'first_name', 'last_name', 'user_ref', 'date_joined',)


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone',)


class ReferalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referal
        fields = '__all__'


class SmsCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsCode
        fields = '__all__'

