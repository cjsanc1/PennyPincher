from django.shortcuts import render, get_object_or_404
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
    return render(request, 'account/detail.html', {
        'account': account
    })

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
    