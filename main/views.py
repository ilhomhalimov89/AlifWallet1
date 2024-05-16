from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    @action(detail=True, methods=['post'])
    def topup(self, request, pk=None):
        wallet = self.get_object()
        amount = request.data.get('amount')
        if amount is not None:
            wallet.balance += amount
            wallet.save()
            transaction = Transaction.objects.create(wallet=wallet, amount=amount)
            return Response({'message': 'Wallet topped up successfully'})
        else:
            return Response({'error': 'Amount not provided'}, status=400)

    @action(detail=True, methods=['get'])
    def balance(self, request, pk=None):
        wallet = self.get_object()
        return Response({'balance': wallet.balance})

    @action(detail=False, methods=['get'])
    def total_transactions(self, request):
        month = timezone.now().month
        year = timezone.now().year
        total_amount = Transaction.objects.filter(date__month=month, date__year=year).aggregate(models.Sum('amount'))
        total_count = Transaction.objects.filter(date__month=month, date__year=year).count()
        return Response({'total_amount': total_amount, 'total_count': total_count})
