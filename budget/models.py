from django.db import models

class Account(models.Model):
	name = models.CharField(max_length=200)
	balance = models.DecimalField(max_digits=8, decimal_places=2)

class ExpenseCategory(models.Model):
	name = models.CharField(max_length=30)

class Transaction(models.Model):
	date = models.DateTimeField()
	category = models.ForeignKey(ExpenseCategory)
	account = models.ForeignKey(Account)
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	memo = models.CharField(max_length=300)
