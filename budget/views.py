from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from decimal import Decimal
from django.core.serializers import serialize
from django.utils import simplejson as json

from budget.models import Transaction, Account, AccountCategory, TransactionForm
import datetime

def month_abbr_to_int(month):
	if month == 'Jan':
		return 1
	if month == 'Feb':
		return 2
	if month == 'Mar':
		return 3
	if month == 'Apr':
		return 4
	if month == 'May':
		return 5
	if month == 'Jun':
		return 6
	if month == 'Jul':
		return 7
	if month == 'Aug':
		return 8
	if month == 'Sep':
		return 9
	if month == 'Oct':
		return 10
	if month == 'Nov':
		return 11
	if month == 'Dec':
		return 12

def get_account_amounts_by_date(account_id, month_str, year_str):
	ret = {}
	month = month_abbr_to_int(month_str)
	year = int(year_str)
	start_date = datetime.date(year, month, 1)
	if (month_str == 'Feb'):
		end_date = datetime.date(year, month, 28)
	elif (month_str in ['Jan', 'Mar', 'May', 'Jul', 'Aug', 'Oct', 'Dec']):
		end_date = datetime.date(year, month, 31)
	else:
		end_date = datetime.date(year, month, 30)
	
	acct = Account.objects.get(pk=account_id)
	
	projections = Transaction.objects.filter(to_account=acct).filter(prediction=True).filter(date__range=(start_date, end_date))
	actuals = Transaction.objects.filter(to_account=acct).filter(prediction=False).filter(date__range=(start_date, end_date))
	
	if projections:
		ret['proj'] = projections[0].amount
	else:
		ret['proj'] = Decimal(0.00)
	
	actual = Decimal(0.0)
	for act in actuals:
		actual += act.amount
	ret['actual'] = actual
	ret['diff'] = ret['proj'] - ret['actual']
	return ret

def map_categories(categories, month, year):
    data = {}
    entries = []
    proj_total = Decimal(0.0)
    act_total = Decimal(0.0)
    for cat in categories:
        entry = {'cat': cat}
        accounts = Account.objects.filter(category=cat)
        all_accounts = []
        for acct in accounts:
            data = get_account_amounts_by_date(acct.id, month, year)
            proj_total += data['proj']
            acct_entry = {'acct': acct, 'pred': data['proj'], 'act': data['actual'], 'diff': data['diff']}
            all_accounts.append(acct_entry)
            act_total += data['actual']
        entry['accounts'] = all_accounts
        entries.append(entry)
    data['categories'] = entries
    data['act_total'] = act_total
    data['proj_total'] = proj_total
    data['difference'] = proj_total - act_total
    return data

def index(request, month=None, year=None):
    today = datetime.date.today()
    if (not month):
        month = today.strftime('%b')
    if (not year):
        year = today.year
    bank_category = AccountCategory.objects.get(name='Bank Accounts')
    context = {'bank_category': {'cat': bank_category, 'accounts': Account.objects.filter(category=bank_category)}}
    context['income_categories'] = map_categories(AccountCategory.objects.filter(income_accounts=True), month, year)
    context['expense_categories'] = map_categories(AccountCategory.objects.filter(income_accounts=False), month, year)
    context['proj_total'] = context['income_categories']['proj_total'] - context['expense_categories']['proj_total'];
    context['act_total'] = context['income_categories']['act_total'] - context['expense_categories']['act_total'];
    context['difference'] = context['expense_categories']['difference'] - context['income_categories']['difference'];
    context['month'] = month
    context['year'] = year
    return render(request, 'budget/index.html', context)

def transaction(request, tid):
    trans = get_object_or_404(Transaction, pk=tid)
    return render(request, 'budget/transaction.html', {'trans': trans})

def account(request, aid):
    account = get_object_or_404(Account, pk=aid)
    transactions = Transaction.objects.filter(to_account=aid).filter(prediction=False) | Transaction.objects.filter(from_account=aid).filter(prediction=False)
    return render(request, 'budget/account.html', {
    	'account': account,
    	'transactions': transactions
    })
    
def category(request, cid):
	category = get_object_or_404(AccountCategory, pk=cid)
	accounts = Account.objects.filter(category=category)
	return render(request, 'budget/category.html', {
		'category': category,
		'accounts': accounts
	})

def addtransaction(request, to_account=None):
    context = {}
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            f = TransactionForm(request.POST)
            trans = f.save(commit = False)
            trans.to_account = Account.objects.get(pk=request.POST['to_account'])
            trans.from_account = Account.objects.get(name="Checking Account")
            trans.prediction = False
            trans.save()
            trans.to_account.balance = trans.to_account.balance + trans.amount
            trans.to_account.save()
            trans.from_account.balance = trans.from_account.balance - trans.amount
            trans.from_account.save()
            return HttpResponseRedirect('/budget/')
    else:
        context['form'] = TransactionForm()
    if to_account:
    	context['to_account'] = Account.objects.get(pk=to_account)
   	return render(request, 'budget/addtransaction.html', context)
   	
def set_projection(request):
	trans = Transaction.objects.filter(to_account=request.POST['account_id']).filter(prediction=True)
	if trans:
		trans = trans[0]
		trans.amount = request.POST['amount']
		trans.save()
	else:
		trans = Transaction()
		trans.to_account = Account.objects.get(pk=request.POST['account_id'])
		trans.from_account = Account.objects.get(name="Checking Account")
		trans.prediction = True
		trans.amount = Decimal(request.POST['amount'])
		trans.memo = 'Projection'
		trans.save()
	#return HttpResponse(serialize('json', (trans,)), mimetype="application/json")
	
	#need to give back the new difference amount
	return HttpResponse(Decimal(trans.amount) - trans.to_account.balance)
