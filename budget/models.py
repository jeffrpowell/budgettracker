from django.db import models

class AccountCategory(models.Model):
	name = models.CharField(max_length=30)
	def __unicode__(self):
                return self.name
	
class Account(models.Model):
	name = models.CharField(max_length=200)
	balance = models.DecimalField(max_digits=8, decimal_places=2)
	category = models.ForeignKey(AccountCategory)
	def __unicode__(self):
                return self.name

class Transaction(models.Model):
	date = models.DateField()
	to_account = models.ForeignKey(Account, related_name="to_account")
	from_account = models.ForeignKey(Account, related_name="from_account")
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	prediction = models.BooleanField()
	memo = models.CharField(max_length=300, default=None, blank=True, null=True)
	def __unicode__(self):
                return unicode(self.amount)
