from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Account, Transaction
from .forms import TransactionForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def accounts_index(request):
    accounts = Account.objects.all()
    return render(request, 'accounts.html', {
        'accounts': accounts
        
        })

def account_detail(request, pk):
    account = get_object_or_404(Account, pk=pk)
    transactions = Transaction.objects.filter(account=account)
    transaction_form = TransactionForm()
    return render(request, 'account/detail.html', {
        'account': account,
        'transactions': transactions,
        'transaction_form': transaction_form
    })

def add_transaction(request, pk):
    form = TransactionForm(request.POST)
    if form.is_valid():
        new_transaction = form.save(commit=False)
        new_transaction.account_id = pk
        new_transaction.save()
    return redirect('account_detail', pk=pk)
    

class AccountCreate(LoginRequiredMixin, CreateView):
    model = Account
    fields = 'name',
    success_url = '/accounts'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class AccountUpdate(UpdateView):
    model = Account
    fields = 'name',
    success_url = '/accounts'

class AccountDelete(DeleteView):
    model = Account
    success_url = '/accounts'
    