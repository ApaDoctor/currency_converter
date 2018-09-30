import re

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from api.models import Currency, ExchangeRate
from webargs import fields

from api.parser import use_args
from currency_converter import settings

in_currencies = lambda x: x in settings.SUPPORTED_CURRENCIES.keys()
converter_args = {
    "input_currency": fields.Str(required=True, validate=in_currencies),
    "amount": fields.Float(required=True, validate=lambda x: x > 0),
    "output_currency": fields.Str(validate=in_currencies)
}


class CurrencyConverter(View):
    """
    Converts currency to other currencies or concrete if selected.
    Input params:
        amount (required) - float or int
        input_currency (required) - currency symbol or currency code
    """

    @use_args(converter_args)
    def get(self, request, args):
        amount = round(args["amount"], 2)
        try:
            # Parse currency
            input_currency = Currency.parse_currency(args["input_currency"])
            output_currency = Currency.parse_currency(args.get("output_currency", None))

            if input_currency == output_currency:
                raise Exception("The input currency can't be equal to the output one")
        except Exception as e:
            return JsonResponse({"error": str(e)}, json_dumps_params={'indent': 2})

        result = ExchangeRate.convert_currency(input_currency, output_currency, amount)

        return JsonResponse({
            'input': {
                'amount': amount,
                'currency': input_currency.code
            },
            'output': result
        }, json_dumps_params={'indent': 2})
