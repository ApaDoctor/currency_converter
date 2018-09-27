from django.test import TestCase

from api.models import Currency, ExchangeRate
from currency_converter import settings

# Create your tests here.
from api.rate_provider import RateProvider


class TestRatesProvider(TestCase):
    def test_appropriate_providers(self):
        for x in RateProvider.ACTIVE_PROVIDERS:
            self.assertTrue(hasattr(RateProvider(), "_{}".format(x)), 'ACTIVE_PROVIDERS variable'
                                                                      ' contains provider which has no method')

    def test_exchange_services_output(self):
        for x in RateProvider.ACTIVE_PROVIDERS:
            data = RateProvider(x).get_current_provider()('USD')

            self.assertIsInstance(data, dict, 'Provider must return dict of currencies with rates')
            for currency, rate in data.items():
                self.assertTrue(isinstance(rate, float) or isinstance(rate, int), 'Rate must be integer or float')

                self.assertTrue(len(currency) == 3, 'Currency code length is 3 characters')
                self.assertIn(currency, settings.SUPPORTED_CURRENCIES.keys(), 'Currency must be one of the supported')

    def test_rateprovider_output(self):
        for x in RateProvider.ACTIVE_PROVIDERS:
            data = RateProvider(x).get_rates()
            self.assertIsInstance(data, dict)
            for key, value in data.items():
                self.assertTrue(isinstance(value, dict) or value is None)
                self.assertIsInstance(key, str)
                self.assertIn(key, settings.SUPPORTED_CURRENCIES.keys())


class TestCurrency(TestCase):
    def test_currency_fill_no_duplicates(self):
        Currency.fill_data()
        currency = len(Currency.objects.all())
        Currency.fill_data()
        currency_after = len(Currency.objects.all())

        self.assertEqual(currency, currency_after)

    def test_currency_fill(self):
        Currency.objects.all.delete()
        Currency.fill_data()
        self.assertTrue(Currency.objects.exists())


class TestExchangeRate(TestCase):
    def test_fill_data(self):
        ExchangeRate.update_rates()
        self.assertTrue(ExchangeRate.objects.exists())
