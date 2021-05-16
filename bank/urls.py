
from django.contrib import admin
from django.urls import path
from .views import UserRegistration,UserLogin,UserLogout,AccountCreate,Deposit,TransactionApi,MoneyTransfer,\
    Withdraw,BalanceCheck,TransactionHistory,CreditedHistory,DebitHistory

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',UserRegistration.as_view()),
    path('login/',UserLogin.as_view()),
    path('logout/',UserLogout.as_view()),
    path('createacc/',AccountCreate.as_view()),
    path('deposit/<int:acc>',Deposit.as_view()),
    path('withdraw/<int:acc>',Withdraw.as_view()),
    path('all_transaction_view/',TransactionApi.as_view()),
    path('money_transfer/',MoneyTransfer.as_view()),
    path('transaction/history/<int:acc>',TransactionHistory.as_view()),
    path('transaction/credithistory/<int:acc>',CreditedHistory.as_view()),
    path("transaction/debitedhistory/<int:acc>",DebitHistory.as_view()),
    path('balancechk/<int:acc>',BalanceCheck.as_view())
]










