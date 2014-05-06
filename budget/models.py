from django.db import models
from django.forms import ModelForm, extras

class AccountCategory(models.Model):
	name = models.CharField(max_length=30)
	income_accounts = models.NullBooleanField()
	goal_accounts = models.BooleanField(default=False)
	def __unicode__(self):
		return self.name
	
class Account(models.Model):
	name = models.CharField(max_length=200)
	balance = models.DecimalField(max_digits=8, decimal_places=2)
	category = models.ForeignKey(AccountCategory)
	goal = models.DecimalField(max_digits=8, decimal_places=2)
	goal_account = models.BooleanField(default=True)
	parent_account = models.ForeignKey('self', related_name="parent_account_", default=None, blank=True, null=True)
	def __unicode__(self):
		return self.name
	def is_income(self):
		return self.category.income_accounts
	def is_goal(self):
		return self.goal_account
	def is_bank(self):
		return self.category.income_accounts == None

class Transaction(models.Model):
	date = models.DateField()
	to_account = models.ForeignKey(Account, related_name="to_account")
	from_account = models.ForeignKey(Account, related_name="from_account")
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	prediction = models.BooleanField()
	memo = models.CharField(max_length=300, default=None, blank=True, null=True)
	def __unicode__(self):
		return "$"+unicode(self.amount)+" : "+self.from_account.name+" -> "+self.to_account.name
                
class TransactionForm(ModelForm):
	class Meta:
		model = Transaction
		fields = ['date', 'amount', 'memo']
		widgets = {
			'date': extras.SelectDateWidget(),
		}
                
class AddTransactionForm(ModelForm):
	class Meta:
		model = Transaction
		fields = ['date', 'from_account', 'amount', 'memo']
		widgets = {
			'date': extras.SelectDateWidget(),
		}
	#http://stackoverflow.com/questions/962226/need-help-with-django-modelform-how-to-filter-foreignkey-manytomanyfield
	def __init__(self, *args, **kwargs):
		super(AddTransactionForm, self).__init__(*args, **kwargs)
		if self.instance:
			bank_category = AccountCategory.objects.get(name='Bank Accounts')
			self.fields['from_account'].queryset = Account.objects.filter(category=bank_category)

class NullAccountTransactionForm(ModelForm):
	class Meta:
		model = Transaction
		fields = ['date', 'from_account', 'to_account', 'amount', 'memo']
		widgets = {
			'date': extras.SelectDateWidget(),
		}
	#http://stackoverflow.com/questions/962226/need-help-with-django-modelform-how-to-filter-foreignkey-manytomanyfield
	def __init__(self, *args, **kwargs):
		super(NullAccountTransactionForm, self).__init__(*args, **kwargs)
		if self.instance:
			bank_category = AccountCategory.objects.get(name='Bank Accounts')
			self.fields['from_account'].queryset = Account.objects.filter(category=bank_category)
			self.fields['to_account'].queryset = Account.objects.filter(category=bank_category)

class AccountForm(ModelForm):
	class Meta:
		model = Account
		fields = ['name', 'balance', 'category', 'parent_account', 'goal', 'goal_account']
	#http://stackoverflow.com/questions/962226/need-help-with-django-modelform-how-to-filter-foreignkey-manytomanyfield
	def __init__(self, *args, **kwargs):
		super(AccountForm, self).__init__(*args, **kwargs)
		if self.instance:
			bank_category = AccountCategory.objects.get(name='Bank Accounts')
			self.fields['parent_account'].queryset = Account.objects.filter(category=bank_category).filter(parent_account=None)