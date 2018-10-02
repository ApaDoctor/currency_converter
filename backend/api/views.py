from django.http import JsonResponse
from django.views import View
from marshmallow import fields, ValidationError

from api.logic import convert_currency
from api.models import Currency, ExchangeRate
from api.parser import use_args
from currency_converter import settings


def validate_currency(x): return x in settings.SUPPORTED_CURRENCIES.keys()


def deserialize_currency(x):
    if not validate_currency(x):
        raise ValidationError('Incorrect currency')
    return Currency.parse_currency(x)


converter_args = {
    "input_currency": fields.Function(required=True, deserialize=deserialize_currency),
    "amount": fields.Float(required=True, validate=lambda x: x > 0),
    "output_currency": fields.Function(deserialize=deserialize_currency)
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

        input_currency = args["input_currency"]
        output_currency = args.get("output_currency", None)

        if input_currency == output_currency:
            return JsonResponse(
                {"error": "The input currency can't be equal to the output one"}
            )

        result = convert_currency(ExchangeRate.get_rates(input_currency, output_currency), amount)

        return JsonResponse({
            'input': {
                'amount': amount,
                'currency': input_currency.code
            },
            'output': result
        }, json_dumps_params={'indent': 2})
