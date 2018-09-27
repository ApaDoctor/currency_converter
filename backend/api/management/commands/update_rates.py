from django.core.management.base import BaseCommand, CommandError

from api.models import Currency, ExchangeRate
from currency_converter import settings
from api.currencies import CURRENCIES
from api.rate_provider import RateProvider


class Command(BaseCommand):
    help = 'Updates database rates with actual data and fills currencies data if there are no them'

    def handle(self, *args, **options):
        # If database is not filled yet we will create new currency objects
        if not Currency.objects.exists():
            print('There are no currencies now, creating...')

            Currency.fill_data()

            print("Currencies have been created")

        print("Updating exchange rates")
        ExchangeRate.update_rates()
        print("Rates are successfully updated.")
