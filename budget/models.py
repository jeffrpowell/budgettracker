from django.db import models
from django.forms import ModelForm

class AccountCategory(models.Model):
	name = models.CharField(max_length=30)
	income_accounts = models.NullBooleanField()
	def __unicode__(self):
		return self.name
	
class Account(models.Model):
	name = models.CharField(max_length=200)
	balance = models.DecimalField(max_digits=8, decimal_places=2)
	category = models.ForeignKey(AccountCategory)
	def __unicode__(self):
		return self.name

class Transaction(models.Model):
	date = models.DateField(auto_now_add=True)
	to_account = models.ForeignKey(Account, related_name="to_account")
	from_account = models.ForeignKey(Account, related_name="from_account")
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	prediction = models.BooleanField()
	memo = models.CharField(max_length=300, default=None, blank=True, null=True)
	def __unicode__(self):
		return unicode(self.amount)
                
class TransactionForm(ModelForm):
    class Meta:
    	model = Transaction
    	fields = ['amount', 'memo']
