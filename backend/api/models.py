from django.db import models


# Create your models here.
class Currency(models.Model):
    class Meta:
        app_label = 'api'
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=35)
    symbol = models.CharField(max_length=10)


class ExchangeRate(models.Model):
    source = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='exchange_source')
    target = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='exchange_target')
    rate = models.FloatField()

