from django.db import models

class AccountCategory(models.Model):
	name = models.CharField(max_length=30)
	def __unicode__(self):
                return self.name
	
class Account(models.Model):
	name = models.CharField(max_length=200)
	balance = models.DecimalField(max_digits=8, decimal_places=2)
	asset_account = models.BooleanField()
	category = models.ForeignKey(AccountCategory)
	def __unicode__(self):
                return self.name

class Transaction(models.Model):
	date = models.DateField()
	debit_account = models.ForeignKey(Account, related_name="debit_account")
	credit_account = models.ForeignKey(Account, related_name="credit_account")
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	memo = models.CharField(max_length=300)
	def __unicode__(self):
                return self.amount
