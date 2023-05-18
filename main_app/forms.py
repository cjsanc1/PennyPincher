from django.forms import ModelForm
from .models import Transaction


class TransactionForm(ModelForm):
  class Meta:
    model = Transaction
    fields = ['user', 'date', 'amount', 'description', 'tags']

    