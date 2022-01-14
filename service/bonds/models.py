from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date

User = get_user_model()

class Bond(models.Model):
    buyer = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, validators=[MinLengthValidator(3)])
    quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)])
    price = models.DecimalField(max_digits=13, decimal_places=4, default=0.0000, validators=[MinValueValidator(0.0000), MaxValueValidator(100000000.0000)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    purchased = models.DateTimeField(null=True, blank=True)
    
    
class MoneyExchangeManager(models.Manager):
    def for_date(self, date_str):
        date = parse_date(date_str)
        query = self.filter(date=date)
        if query.exists():
            return query.first
        MoneyExchange = self.model   
    
    
class MoneyExchange(models.Model):
    date = models.DateField()
    # USD/MXN
    rate = models.DecimalField(max_digits=5, decimal_places=4)
    created = models.DateTimeField(auto_now_add=True)
    objects = MoneyExchangeManager()
    
    
    def is_sold(self):
        return self.buyer_id is not None