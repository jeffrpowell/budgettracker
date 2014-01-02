from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from decimal import Decimal

from budget.models import Transaction, Account, AccountCategory, TransactionForm

def index(request):
    categories = AccountCategory.objects.all().exclude(name='Bank Accounts')
    bank_category = AccountCategory.objects.get(name='Bank Accounts')
    context = {'bank_category': {'cat': bank_category, 'accounts': Account.objects.filter(category=bank_category)}}
    data = []
    for cat in categories:
        entry = {'cat': cat}
        accounts = Account.objects.filter(category=cat)
        all_accounts = []
        for acct in accounts:
            projections = Transaction.objects.filter(to_account=acct).filter(prediction=True)
            proj_total = Decimal(0.0)
            for proj in projections:
                proj_total = proj_total + proj.amount
            acct_entry = {'acct': acct, 'pred': proj_total, 'diff': proj_total-acct.balance}
            all_accounts.append(acct_entry)
        entry['accounts'] = all_accounts
        data.append(entry)
    context['data'] = data
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