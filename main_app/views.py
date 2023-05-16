from django.shortcuts import render
from .models import Account, Transaction
from .forms import TransactionForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def accounts_index(request):
    return render(request, 'accounts.html')

def accounts_detail(request, account_id):
    account = Account.objects.get(id=account_id)
    transaction_form = TransactionForm()
    return render(request, 'accounts/detail.html', {
        'account': account, 'transaction_form': transaction_form
    })
