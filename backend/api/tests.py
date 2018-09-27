from django.test import TestCase

from api.models import Currency, ExchangeRate
from currency_converter import settings

# Create your tests here.
from api.rate_provider import RateProvider

from django.test import Client


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
    def setUp(self):
        Currency.fill_data()

    def test_currency_fill_no_duplicates(self):
        Currency.fill_data()
        currency = Currency.objects.all()
        Currency.fill_data()
        currency_after = Currency.objects.all()

        self.assertEqual(len(currency), len(currency_after))

    def test_currency_fill(self):
        Currency.objects.all().delete()
        Currency.fill_data()
        self.assertTrue(Currency.objects.exists())

    def test_parse_incorrect_symbol_currency(self):
        def failure():
            Currency.parse_currency("$$")

        self.assertRaises(Currency.DoesNotExist, failure)

    def test_parse_currency(self):
        print(Currency.objects.all())

        self.assertEqual(Currency.parse_currency('£'), Currency.parse_currency('GBP'))
        self.assertEqual(Currency.parse_currency('¥'), Currency.parse_currency('CNY'))
        self.assertEqual(Currency.parse_currency('€'), Currency.parse_currency('EUR'))

    def part_multiple_result(self):
        if len(Currency.objects.filter(code='$')) > 1:
            self.assertRaises(Currency.MultipleObjectsReturned, Currency.parse_currency, '$')


class TestExchangeRate(TestCase):
    def setUp(self):
        ExchangeRate.update_rates()

    def test_fill_data(self):
        ExchangeRate.update_rates()

    def test_get_rates(self):
        data = ExchangeRate.get_rates('USD')
        self.assertIsInstance(data, dict, 'Provider must return dict of currencies with rates')
        for currency, rate in data.items():
            self.assertTrue(isinstance(rate, float) or isinstance(rate, int), 'Rate must be integer or float')

            self.assertTrue(len(currency) == 3, 'Currency code length is 3 characters')
            self.assertIn(currency, settings.SUPPORTED_CURRENCIES.keys(), 'Currency must be one of the supported')


class TestConverter(TestCase):
    def setUp(self):
        Currency.fill_data()
        ExchangeRate.update_rates()

    def test_incorrect_input_currency(self):
        c = Client()
        r = c.get('/currency_converter', {'input_currency': 'USDT', "amount": 1})
        self.assertIsNotNone(r.json().get('error'))

    def test_incorrect_method(self):
        c = Client()
        response = c.post('/currency_converter', {'input_currency': "USD", "amount": 1})
        self.assertTrue(response.status_code == 405)

    def test_incorrect_output_currency(self):
        c = Client()
        r = c.get('/currency_converter', {'input_currency': 'USD', "amount": 1, "output_currency": "USDT"})
        self.assertIsNotNone(r.json().get('error'))

    def test_same_output_input_currencies(self):
        c = Client()
        r = c.get('/currency_converter', {'input_currency': 'USD', "amount": 1, "output_currency": "USD"})
        self.assertIsNotNone(r.json().get('error'))

    def test_amount(self):
        c = Client()
        x = -0.5
        while x < 0:
            r = c.get('/currency_converter', {'input_currency': 'USD', "amount": x})
            self.assertIsNotNone(r.json().get('error'))
            x += 0.01

        x = 0
        while x < 10:
            r = c.get('/currency_converter', {'input_currency': 'USD', "amount": x})
            self.assertIsNone(r.json().get('error'))
            x+=0.5123348723462334534


        r = c.get('/currency_converter', {'input_currency': 'USD', "amount": "asdasdasda"})
        self.assertIsNotNone(r.json().get('error'))

        r = c.get('/currency_converter', {'input_currency': 'USD', "amount": "123123sad"})
        self.assertIsNotNone(r.json().get('error'))

        r = c.get('/currency_converter', {'input_currency': 'USD', "amount": "1231231zsdsda123123"})
        self.assertIsNotNone(r.json().get('error'))

        r = c.get('/currency_converter', {'input_currency': 'USD', "amount": "."})
        self.assertIsNotNone(r.json().get('error'))