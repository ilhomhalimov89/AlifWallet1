from django.db import models


class Wallet(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    is_identified = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
