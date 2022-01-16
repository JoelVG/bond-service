from datetime import date
from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator)
from django.db import models
from bonds.utils import currency_exchange

User = get_user_model()

class BondManager(models.Manager):
    
    def get_usd(self, queryset):
        rate = MoneyExchange.objects.for_date(date.today())
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
    
    def for_date(self, date):
        query = self.filter(date=date)
        if query.exists():
            return query.first()
        rate = currency_exchange(date)   
        instance = self.create(date=date, rate=rate)
        return instance
        
    
class MoneyExchange(models.Model):
    date = models.DateField()
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    created = models.DateTimeField(auto_now_add=True)
    objects = MoneyExchangeManager()