from django.contrib import admin
from budget.models import AccountCategory, Account, Transaction

admin.site.register(AccountCategory)
admin.site.register(Account)
admin.site.register(Transaction)
