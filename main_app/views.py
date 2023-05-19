from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Account, Transaction, Tag
from .forms import TransactionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def accounts_index(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'accounts.html', {
        'accounts': accounts
        
        })

@login_required
def account_detail(request, pk):
    account = get_object_or_404(Account, pk=pk)
    transactions = Transaction.objects.filter(account=account)
    transaction_form = TransactionForm()
    tags = Tag.objects.filter(transaction__account=account).distinct()
    return render(request, 'account/detail.html', {
        'account': account,
        'transactions': transactions,
        'transaction_form': transaction_form,
        'tags': tags
    })

@login_required
def add_transaction(request, pk):
    form = TransactionForm(request.POST)
    selected_values = request.POST.getlist("tags")
    print(selected_values)
    if form.is_valid():
        new_transaction = form.save(commit=False)
        new_transaction.account_id = pk
        new_transaction.user = request.user
        new_transaction.save()
        for selected_value in selected_values: 
         new_transaction.tags.add(selected_value) 
    return redirect('account_detail', pk=pk)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('accounts')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
    

class AccountCreate(LoginRequiredMixin, CreateView):
    model = Account
    fields = 'name',
    success_url = '/accounts'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class AccountUpdate(LoginRequiredMixin, UpdateView):
    model = Account
    fields = 'name',
    success_url = '/accounts'

class AccountDelete(LoginRequiredMixin, DeleteView):
    model = Account
    success_url = '/accounts'


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    fields = 'date', 'amount', 'description', 'tags',
    def get_success_url(self):
        # Get the primary key of the account associated with the updated transaction
        account_pk = self.object.account.pk
        # Construct the URL for the account detail page
        success_url = reverse_lazy('account_detail', kwargs={'pk': account_pk})
        return success_url

class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    def get_success_url(self):
        # Get the primary key of the account associated with the updated transaction
        account_pk = self.object.account.pk
        # Construct the URL for the account detail page
        success_url = reverse_lazy('account_detail', kwargs={'pk': account_pk})
        return success_url
    
@login_required
def assoc_tag(request, transaction_id, tag_id):
  Transaction.objects.get(id=transaction_id).tags.add(tag_id)
  return redirect('account_detail', pk=transaction_id)

# def unassoc_toy(request, cat_id, toy_id):
#   Cat.objects.get(id=cat_id).toys.remove(toy_id)
#   return redirect('detail', cat_id=cat_id)