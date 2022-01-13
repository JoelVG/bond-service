from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator   
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date

User = get_user_model()

class Bond(models.Model):
    buyer = models.ForeignKey(User, null=True)
    seller = models.ForeignKey(User)
    name = models.CharField(min_length=3, max_length=40)
    quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)])
    price = models.DecimalField(decimal_places=4, default=0.0000, validators=[MinValueValidator(0.0000), MaxValueValidator(100000000.0000)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    purchased = models.DateTimeField()
    
    
class MoneyExchangeManager(models.Manager):
    def for_date(self, date_str):
        date = parse_date(date_str)
        query = self.filter(date=date)
        if query.exists():
            return query.first
        MoneyExchange = self.model 
        #TODO call api, create obj y return obj    
    
    
class MoneyExchange(models.Model):
    date = models.DateField()
    # USD/MXN
    rate = models.DecimalField()
    created = models.DateTimeField(auto_now_add=True)
    objects = MoneyExchangeManager()
    
    
    def is_sold(self):
        return self.buyer_id is not None