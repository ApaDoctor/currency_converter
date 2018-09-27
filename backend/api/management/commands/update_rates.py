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
            create_queue = []

            # Fill list with Currency objects
            for cur_code in settings.SUPPORTED_CURRENCIES:
                if cur_code in CURRENCIES.keys():
                    create_queue.append(Currency(**CURRENCIES[cur_code]))

            # Save all currencies together
            Currency.objects.bulk_create(create_queue)

            print("Currencies have been created")

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

        ExchangeRate.objects.bulk_create(create_queue)

        print("Rates are successfully created.")
