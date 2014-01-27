from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from decimal import Decimal
from django.core.serializers import serialize
from django.utils import simplejson as json

from budget.models import Transaction, Account, AccountCategory, TransactionForm, NullAccountTransactionForm, AddAccountForm
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

def start_end_days_of_month(month_str, year_str):
	month = month_abbr_to_int(month_str)
	year = int(year_str)
	start_date = datetime.date(year, month, 1)
	if (month_str == 'Feb'):
		end_date = datetime.date(year, month, 28)
	elif (month_str in ['Jan', 'Mar', 'May', 'Jul', 'Aug', 'Oct', 'Dec']):
		end_date = datetime.date(year, month, 31)
	else:
		end_date = datetime.date(year, month, 30)
	return [start_date, end_date]

def get_account_amounts_by_date(account_id, month_str, year_str):
	ret = {}
	
	dates = start_end_days_of_month(month_str, year_str)
	
	acct = Account.objects.get(pk=account_id)
	
	if (acct.category.income_accounts == None):
		deposits = Transaction.objects.filter(to_account=acct).filter(prediction=False).filter(date__range=(dates[0], dates[1]))
		withdrawals = Transaction.objects.filter(from_account=acct).filter(prediction=False).filter(date__range=(dates[0], dates[1]))
		balance = Decimal(0.0)
		for dep in deposits:
			balance += dep.amount
		for wit in withdrawals:
			balance -= wit.amount
		ret['actual'] = balance
	else:
		projections = Transaction.objects.filter(to_account=acct).filter(prediction=True).filter(date__range=(dates[0], dates[1]))
		if acct.is_income():
			actuals = Transaction.objects.filter(from_account=acct).filter(prediction=False).filter(date__range=(dates[0], dates[1]))
		else:
			actuals = Transaction.objects.filter(to_account=acct).filter(prediction=False).filter(date__range=(dates[0], dates[1]))
	
		if projections:
			ret['proj'] = projections[0].amount
		else:
			ret['proj'] = Decimal(0.00)
	
		actual = Decimal(0.0)
		for act in actuals:
			actual += act.amount
		ret['actual'] = actual
		if acct.is_income():
			ret['diff'] = ret['actual'] - ret['proj']
		else:
			ret['diff'] = ret['proj'] - ret['actual']
	return ret

def map_categories(categories, month, year, income):
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
    if income:
        data['difference'] = act_total - proj_total
    else:
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
    context['income_categories'] = map_categories(AccountCategory.objects.filter(income_accounts=True), month, year, True)
    context['expense_categories'] = map_categories(AccountCategory.objects.filter(income_accounts=False), month, year, False)
    context['proj_total'] = context['income_categories']['proj_total'] - context['expense_categories']['proj_total'];
    context['act_total'] = context['income_categories']['act_total'] - context['expense_categories']['act_total'];
    context['difference'] = context['expense_categories']['difference'] - context['income_categories']['difference'];
    context['month'] = month
    context['year'] = year
    return render(request, 'budget/index.html', context)

def transaction(request, tid, aid):
    trans = get_object_or_404(Transaction, pk=tid)
    context = {}
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            old_trans = Transaction.objects.get(id=tid)
            old_amount = trans.amount
            f = TransactionForm(request.POST)
            new_trans = f.save(commit = False)
            trans.prediction = False
            if old_trans.from_account.is_income():
                old_trans.from_account.balance = old_trans.from_account.balance - old_amount + new_trans.amount
            else:
                old_trans.from_account.balance = old_trans.from_account.balance + old_amount - new_trans.amount
            old_trans.to_account.balance = old_trans.to_account.balance - old_amount + new_trans.amount
            old_trans.to_account.save()
            old_trans.from_account.save()
            old_trans.amount = new_trans.amount
            old_trans.memo = new_trans.memo
            old_trans.save()
            
            return HttpResponseRedirect('/budget/account/'+aid)
    else:
        context['form'] = TransactionForm()
        context['trans'] = trans
        context['acct'] = get_object_or_404(Account, pk=aid)
        context['category'] = context['acct'].category
    return render(request, 'budget/transaction.html', context)

def account(request, aid, month=None, year=None):
    account = get_object_or_404(Account, pk=aid)
    today = datetime.date.today()
    if (not month):
        month = today.strftime('%b')
    if (not year):
        year = today.year
    dates = start_end_days_of_month(month, year)
    
    transactions = Transaction.objects.filter(to_account=aid).filter(prediction=False).filter(date__range=(dates[0], dates[1])) | Transaction.objects.filter(from_account=aid).filter(prediction=False).filter(date__range=(dates[0], dates[1]))
    
    amounts = get_account_amounts_by_date(aid, month, year)
    return render(request, 'budget/account.html', {
    	'account': account,
    	'transactions': transactions,
    	'balance': amounts['actual'],
    	'month': month,
    	'year': year,
    })

def addaccount(request, cid=None):
    context = {}
    if request.method == 'POST':
        form = AddAccountForm(request.POST)
        if form.is_valid():
            f = AddAccountForm(request.POST)
            acct = f.save(commit = False)
            acct.category = AccountCategory.objects.get(pk=cid)
            acct.balance = 0
            acct.save()
            return HttpResponseRedirect('/budget/')
    else:
        context['form'] = AddAccountForm()
        context['category'] = get_object_or_404(AccountCategory, pk=cid)
   	return render(request, 'budget/addaccount.html', context)
   	
def deleteaccount(request, aid):
    acct = Account.objects.get(pk=aid)
    acct.delete()
    return HttpResponseRedirect('/budget/')
    
def category(request, cid):
	category = get_object_or_404(AccountCategory, pk=cid)
	accounts = Account.objects.filter(category=category)
	return render(request, 'budget/category.html', {
		'category': category,
		'accounts': accounts
	})

def addtransaction(request, to_account):
    context = {}
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            f = TransactionForm(request.POST)
            trans = f.save(commit = False)
            trans.prediction = False
            account = Account.objects.get(pk=to_account)
            if account.is_income():
                trans.to_account = trans.from_account
                trans.from_account = account
                trans.save()
                trans.from_account.balance = trans.from_account.balance + trans.amount
            else:
                trans.to_account = account
                #trans.from_account already set through form
                trans.save()
                trans.from_account.balance = trans.from_account.balance - trans.amount
            trans.to_account.balance = trans.to_account.balance + trans.amount
            trans.to_account.save()
            trans.from_account.save()
            return HttpResponseRedirect('/budget/')
    else:
        context['form'] = TransactionForm()
    template = 'budget/addtransaction.html'
    if to_account:
    	context['account'] = Account.objects.get(pk=to_account)
    	if context['account'].is_income():
    	    template = 'budget/adddeposit.html'
   	return render(request, template, context)

def banktransaction(request):
    context = {}
    if request.method == 'POST':
        form = NullAccountTransactionForm(request.POST)
        if form.is_valid():
            f = NullAccountTransactionForm(request.POST)
            trans = f.save(commit = False)
            trans.prediction = False
            trans.save()
            trans.to_account.balance = trans.to_account.balance + trans.amount
            trans.to_account.save()
            trans.from_account.balance = trans.from_account.balance - trans.amount
            trans.from_account.save()
            return HttpResponseRedirect('/budget/')
    else:
        context['form'] = NullAccountTransactionForm()
   	return render(request, 'budget/banktransaction.html', context)

def transaction_delete(request, tid):
	trans = get_object_or_404(Transaction, pk=tid)
	if trans.from_account.is_income():
		trans.from_account.balance = trans.from_account.balance - trans.amount
		redir = '/budget/account/' + str(trans.from_account.id)
	else:
		trans.from_account.balance = trans.from_account.balance + trans.amount
		redir = '/budget/account/' + str(trans.to_account.id)
	trans.to_account.balance = trans.to_account.balance - trans.amount
	trans.from_account.save()
	trans.to_account.save()
	trans.delete()
	return HttpResponseRedirect(redir)
	
   	
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
	amounts = get_account_amounts_by_date(trans.to_account.id, request.POST['month'], request.POST['year'])
	return HttpResponse(amounts['diff'])
