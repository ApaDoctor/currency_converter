from django.db import models

from api.currencies import CURRENCIES
from api.rate_provider import RateProvider
from currency_converter import settings


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

    @classmethod
    def fill_data(cls):
        """
        Fills DATABASE with the currencies listed in SUPPORTED_CURRENCIES field in the settings.
        Doesn't delete existing data. So it's up to you delete it or not.
        """

        create_queue = []
        current_currencies = [x.code for x in Currency.objects.all()]
        # Fill list with Currency objects
        for cur_code in settings.SUPPORTED_CURRENCIES:
            if cur_code in CURRENCIES.keys() and cur_code not in current_currencies:
                create_queue.append(Currency(**CURRENCIES[cur_code]))

        # Save all currencies together
        cls.objects.bulk_create(create_queue)


class ExchangeRate(models.Model):
    """
    Stores exchange rate for with two different :model:`api.Currency`
    """
    source = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='exchange_source')
    target = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='exchange_target')
    rate = models.FloatField()

    def __str__(self):
        return "{} -> {}".format(self.source, self.target)

    @classmethod
    def update_rates(cls):
        """
        Updates rates with fresh data from provider selected in the settings EXCHANGE_RATE_PROVIDER
        """

        # Its faster to get whole QuerySet and call get from it then call .get() each time
        currencies = Currency.objects.all()

        # Clear all rates to replace it with updated
        ExchangeRate.objects.all().delete()

        create_queue = []

        for source, rates in RateProvider().get_rates().items():

            try:
                source = currencies.get(code=source)
            except Currency.DoesNotExist:
                continue

            # If there are no rates for currency - we skip it
            if rates is None:
                continue

            for target, rate in rates.items():
                target = currencies.get(code=target)

                create_queue.append(ExchangeRate(source=source, target=target, rate=rate))

        # And then create new
        ExchangeRate.objects.bulk_create(create_queue)
