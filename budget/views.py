from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic

from budget.models import Transaction, Account, AccountCategory

def index(request):
    categories = AccountCategory.objects.all().exclude(name='Bank Accounts')
    bank_category = AccountCategory.objects.get(name='Bank Accounts')
    context = {'bank_category': {'cat': bank_category, 'accounts': Account.objects.filter(category=bank_category)}}
    data = []
    for cat in categories:
    	entry = {'cat': cat}
    	entry['accounts'] = Account.objects.filter(category=cat)
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

def addtransaction(request):
    return HttpResponse("You're voting on poll.")
