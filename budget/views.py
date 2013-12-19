from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from budget.models import Transaction

def index(request):
    latest_transaction_list = Transaction.objects.order_by('-id')[:5]
    context = {'latest_transaction_list': latest_transaction_list}
    return render(request, 'budget/index.html', context)

def detail(request, tid):
    trans = get_object_or_404(Transaction, pk=tid)
    return render(request, 'budget/detail.html', {'trans': trans})

def results(request, tid):
    return HttpResponse("You're looking at the results of poll %s." % tid)

def addtransaction(request):
    return HttpResponse("You're voting on poll.")
