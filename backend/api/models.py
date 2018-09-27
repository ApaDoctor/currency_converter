from django.db import models
from django.db.models import Q

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

    @classmethod
    def correct_currencies(cls):
        """
        :return: list of correct values for currency parsers
        """
        correct_cur = set()
        for x in Currency.objects.all():
            correct_cur.add(x.code)
            correct_cur.add(x.symbol)
        return correct_cur

    @classmethod
    def parse_currency(cls, source):
        """
        Method is created to get currency with currency symbol or currency code.
        Currency.MultipleReturned and Currency.DoesntExist exceptions are not excepted.
        There can be few currencies with the same symbol.
        :param source: currency 3-chars code or currency symbol
        :return: Currency object
        """
        return cls.objects.get(Q(symbol=source) | Q(code=source))


class ExchangeRate(models.Model):
    """
    Stores exchange rate for with two different :model:`api.Currency`
    """
    source = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='exchange_source')
    target = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='exchange_target')
    rate = models.FloatField()

    class Meta:
        unique_together = ['source', 'target']

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

    @staticmethod
    def _check_currency(currency):
        """
        Check if selected currency is supported
        If not raise exception
        :param currency: code of currency
        """
        if not (currency in settings.SUPPORTED_CURRENCIES.keys() or isinstance(currency, Currency)):
            raise ValueError("Unsupported currency")

    @classmethod
    def get_rates(cls, source):
        """
        Get exchange rates for selected currency
        :param source: 3-characters code of currency or :model:`api.Currency` object
        :return: dict of exchange rates for selected currency
        """
        cls._check_currency(source)

        data = {'source': source} if isinstance(source, cls) else {"source__code": source}
        return {x.target.code: x.rate for x in cls.objects.filter(**data)}

    @classmethod
    def get_rate(cls, source, target):
        """
        Get exchange rates from one currency to another
        :param source: :model:`api.Currency` object
        :param target: :model:`api.Currency` object
        :return: exchange rate
        """
        cls._check_currency(source)

        return cls.objects.get(source=source, target=target).rate
