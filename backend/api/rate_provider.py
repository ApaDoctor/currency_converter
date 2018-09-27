import requests
from currency_converter import settings

class RateProvider:
    """
    Rate provider uses selected API to get actual exchange rates for all supported currencies
    """
    ACTIVE_PROVIDERS = ['ratesapi', ]

    def __init__(self, provider='ratesapi'):
        if provider not in RateProvider.ACTIVE_PROVIDERS:
            raise ValueError(
                "Unknown provider. Possible are: {}".format(", ".join([x for x in RateProvider.ACTIVE_PROVIDERS])))
        self.provider = provider

    # Methods for supported providers.
    # To add a provider just add new method and register it in the ACTIVE_PROVIDERS variable
    @staticmethod
    def _ratesapi(currency):
        """
        Returns dict of exchange rates for chosen currency
        """
        response = requests.get('https://ratesapi.io/api/latest', {'base': currency}).json()
        return response['rates'] if not response.get("error", False) else None

    @staticmethod
    def _exchangeratesapi(currency):
        response = requests.get('https://api.exchangeratesapi.io/api/latest', {'base': currency}).json()
        return response['rates'] if not response.get("error", False) else None

    def get_current_provider(self):
        """
        Chooses provider method for given provider
        :return: provider method
        """
        try:
            return getattr(self, '_{}'.format(self.provider))
        except AttributeError:
            raise ValueError('Method for provider {} is not defined. Add it to the RateProvider with the same name')

    def get_rates(self):
        """
        Calls chosen provider to get exchange rates
        :return: Dict of all exchange rates.
        """
        provider = self.get_current_provider()
        return {x: provider(x) for x in settings.SUPPORTED_CURRENCIES}
