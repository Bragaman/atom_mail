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


class MonthStatSerializer(serializers.Serializer):
    month = serializers.CharField(max_length=16)
    amount = serializers.DecimalField(max_digits=8, decimal_places=2)
