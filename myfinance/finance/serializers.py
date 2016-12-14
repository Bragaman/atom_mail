from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer
from finance.models import *


class ChargeSerializer(ModelSerializer):
    class Meta:
        model = Charge
        fields = ('id',
                  'account',
                  'value',
                  'date'
                  )


class AccountSerializer(ModelSerializer):
    charges = ChargeSerializer(many=True, read_only=False)
    class Meta:
        model = Account
        fields = (
            'id',
            'name',
            'number',
            'charges'
        )


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'phone_number', 'address',)


class UserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    profile = UserProfileSerializer(many=False, read_only=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_active', 'is_superuser',
                  'date_joined', 'profile')
        extra_kwargs = {'password': {'write_only': True}}



class MonthStatSerializer(serializers.Serializer):
    month = serializers.CharField(max_length=16)
    amount = serializers.DecimalField(max_digits=8, decimal_places=2)
