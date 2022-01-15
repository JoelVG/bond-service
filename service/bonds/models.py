from datetime import date

from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator)
from django.db import models
from django.utils.dateparse import parse_date

from bonds.utils import currency_exchange

User = get_user_model()

class BondManager(models.Manager):
    def get_usd(self):
        rate = MoneyExchange.objects.for_date(date.today())
        queryset = self.get_queryset()
        for q in queryset:
            q.price = q.price/rate.rate
        return queryset
            
            
class Bond(models.Model):
    buyer = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    seller = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, validators=[MinLengthValidator(3)])
    quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)])
    price = models.DecimalField(max_digits=13, decimal_places=4, default=0.0000, validators=[MinValueValidator(0.0000), MaxValueValidator(100000000.0000)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    purchased = models.DateTimeField(null=True, blank=True)
    objects = BondManager()
    

class MoneyExchangeManager(models.Manager):
    
    def for_date(self, date_str):
        date = parse_date(date_str)
        query = self.filter(date=date)
        if query.exists():
            return query.first
        instance = self.create(date=date_str, rate=currency_exchange(date_str.isoformat()))
        return instance
        
    
class MoneyExchange(models.Model):
    date = models.DateField()
    # USD/MXN
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    created = models.DateTimeField(auto_now_add=True)
    objects = MoneyExchangeManager()
    
    def is_sold(self):
        return self.buyer_id is not None