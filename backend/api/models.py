from django.db import models


# Create your models here.
class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=35)


class ExchangeRate(models.Model):
    source = models.ForeignKey(Currency, on_delete=models.PROTECT)
    target = models.ForeignKey(Currency, on_delete=models.PROTECT)
    rate = models.FloatField()

