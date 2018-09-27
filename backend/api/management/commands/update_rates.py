from django.core.management.base import BaseCommand, CommandError

from api.models import Currency
from currency_converter import settings
from api.currencies import CURRENCIES

def get_rates_for_currency(currency_code):
    pass


class Command(BaseCommand):
    help = 'Updates database rates with actual data and fills currencies data if there are no them'

    def handle(self, *args, **options):

        # If database is not filled yet we will create new currency objects
        if Currency.objects.exists():
            create_queue = []

            # Fill list with Currency objects
            for cur_code in settings.SUPPORTED_CURRENCIES:
                create_queue.append(Currency(**CURRENCIES[cur_code]))

            # Save all currencies together
            Currency.objects.bulk_create(create_queue)


        for cur_code in settings.SUPPORTED_CURRENCIES:
            pass
