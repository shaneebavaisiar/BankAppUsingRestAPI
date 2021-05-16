from django.contrib import admin

# Register your models here.
from .models import Accounts,Transaction
admin.site.register(Accounts)
admin.site.register(Transaction)