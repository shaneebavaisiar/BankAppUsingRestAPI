from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from bank.models import Accounts,Transaction


class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

class AccountSerializer(ModelSerializer):
    class Meta:
        model=Accounts
        fields='__all__'


class TransactionSeraializer(ModelSerializer):
    class Meta:
        model=Transaction
        fields=['from_ac_num','to_ac_num','amount','debit_credit']


class DepositSerialiezer(serializers.Serializer):
    # ac_num=serializers.IntegerField()
    amount=serializers.IntegerField()