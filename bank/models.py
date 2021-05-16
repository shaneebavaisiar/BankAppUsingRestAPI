from django.db import models

# Create your models here.
from django.db import models

class Accounts(models.Model):
    ac_num=models.IntegerField(unique=True)
    choices=[
        ('Current account','Current account'),
        ('Savings account','Savings account '),
        ('NRI accounts','NRI accounts')
    ]
    ac_type = models.CharField(max_length=120,choices=choices,default="Current account")
    balance=models.IntegerField()
    user=models.CharField(max_length=120)

    def __str__(self):
        return str(self.ac_num)


class Transaction(models.Model):
    from_ac_num=models.ForeignKey(Accounts,on_delete=models.CASCADE)
    to_ac_num=models.CharField(max_length=40)
    amount=models.IntegerField()
    choices=choices=[
        ('Debited','Debited'),
        ('Credited','Credited'),
    ]
    debit_credit=models.CharField(choices=choices,default="Credited",max_length=20)
    transaction_date=models.DateField(auto_now=True)

    def __str__(self):
        return str(self.from_ac_num)
