from django.db import models


class Currency(models.Model):
    """
    Currency is model used to identify different currencies with special symbols or unique 3 characters code.
    Currencies are connected with :model:`api.ExchangeRate` were stored exchange rate for two currencies
    """

    class Meta:
        app_label = 'api'

    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=35)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.code


class ExchangeRate(models.Model):
    """
    Stores exchange rate for with two different :model:`api.Currency`
    """
    source = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='exchange_source')
    target = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='exchange_target')
    rate = models.FloatField()

    def __str__(self):
        return "{} -> {}".format(self.source, self.target)
