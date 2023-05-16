from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0) #shows balance for given account

    def __str__(self):
        return self.name
    def update_balance(self):
        transactions = self.transaction_set.all()
        total_balance = transactions.aggregate(models.Sum('amount'))['amount__sum'] #calculates balance
        self.balance = total_balance or 0
        self.save() #saves everything
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user.username} - {self.date} - {self.amount}'

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs): #code to save the amount and apply it to account
        super().save(*args, **kwargs) #super() lets you execute original use of save() method this is where it actually gets saved
        self.account.update_balance() #calls function from above