from django.shortcuts import render
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserRegSerializer,LoginSerializer,AccountSerializer,TransactionSeraializer,DepositSerialiezer
from django.contrib.auth import authenticate,login,logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from bank.models import Accounts,Transaction
from rest_framework.permissions import IsAuthenticated


# =====================================user============================================
class UserRegistration(generics.GenericAPIView,mixins.CreateModelMixin,mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserRegSerializer
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request, *args, **kwargs)

class UserLogin(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data.get('username')
            password=serializer.validated_data.get('password')
            # user=authenticate(request,username=username,password=password)
            user=User.objects.get(username=username)
            if(user.username==username) &(user.password==password):
                login(request,user)
                token,created=Token.objects.get_or_create(user=user)
                return Response({'token':token.key},status=204)
            return Response('failed')

class UserLogout(APIView):
    def get(self,request):
        logout(request)
        request.user.auth_token.delete()
# ============================================end user======================================

class AccountCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        account=Accounts.objects.all().last()
        if account:
            last_acc=account.ac_num
            acc_numbr=int(last_acc)+1
        else:
            acc_numbr='1000'
        return Response({'ac_num':acc_numbr})
    def post(self,request):
        serializer=AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=401)


class Deposit(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request,acc):
        serializer=DepositSerialiezer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data.get("amount")
            object = Accounts.objects.get(ac_num=acc)
            if object:
                object.balance+=amount
                object.save()
                return Response({'hello user ':str(amount)+'is deposited and available balance is '+str(object.balance)})
            else:
                return Response('no accout nbr')
        else:
            return Response('failed')

class Withdraw(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request,acc):
        serializer=DepositSerialiezer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data.get("amount")
            object = Accounts.objects.get(ac_num=acc)
            if object:
                if object.balance>amount:
                    object.balance-=amount
                    object.save()
                    return Response({'hello user':str(amount)+' is debited and available balance is '+str(object.balance)})
                else:
                    return Response('no available balance')
            else:
                return Response('no account nbr')
        else:
            return Response('failed')

class BalanceCheck(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,acc):
        acc=Accounts.objects.get(ac_num=acc)
        balance=acc.balance
        return Response({'available balance is':str(balance)})



class MoneyTransfer(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        transaction = Transaction.objects.all()
        serializer = TransactionSeraializer(transaction, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer=TransactionSeraializer(data=request.data)
        print(request.data)
        print(serializer)
        if serializer.is_valid():
            from_ac_num=serializer.validated_data.get("from_ac_num")
            to_ac_num=serializer.validated_data.get("to_ac_num")
            amount=serializer.validated_data.get("amount")
            debit_credit=serializer.validated_data.get("debit_credit")
            acc = Accounts.objects.get(ac_num=from_ac_num)
            if acc:
                transfer=Transaction(from_ac_num=acc,to_ac_num=to_ac_num,amount=amount,debit_credit=debit_credit)
                transfer.save()
                if debit_credit=='Debited':
                    if acc.balance>amount:
                        acc.balance-=amount
                        acc.save()
                        return Response({"Hello user":str(amount)+' has been debited and available balance:'+str(acc.balance)})
                    else:
                        return Response('no available balance')
                elif debit_credit=='Credited':
                    acc.balance+=amount
                    acc.save()
                    return Response({"Hello user": str(amount) + ' has been credited and available balance:' + str(acc.balance)})
            else:
                return Response('no accout')
        else:
            return Response('failed')

class TransactionHistory(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,acc):
        # account=Accounts.objects.get(ac_num=acc)
        transaction_history=Transaction.objects.filter(from_ac_num__ac_num=acc)
        serializer=TransactionSeraializer(transaction_history,many=True)
        return Response(serializer.data)

class CreditedHistory(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,reequest,acc):
        transaction_history = Transaction.objects.filter(from_ac_num__ac_num=acc).filter(debit_credit__exact="Credited")
        serializer = TransactionSeraializer(transaction_history, many=True)
        return Response(serializer.data)

class DebitHistory(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, reequest, acc):
        transaction_history = Transaction.objects.filter(from_ac_num__ac_num=acc).filter(debit_credit__exact="Debited")
        serializer = TransactionSeraializer(transaction_history, many=True)
        return Response(serializer.data)






