import re

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from api.models import Currency, ExchangeRate


class CurrencyConverter(View):
    """
    Converts currency to other currencies or concrete if selected.
    Input params:
        amount (required) - float or int
        input_currency (required) - currency symbol or currency code
    """

    def get(self, request, *args, **kwargs):
        amount = request.GET.get('amount')
        input_currency = request.GET.get('input_currency')
        output_currency = request.GET.get('output_currency')
        message = False

        # Check for errors
        errors = [
            [amount is None or input_currency is None, "Required arguments are missing"
                                                       " - input_currency or output_currency"],
            [re.match(r"^\+?\d*?\.?\d+?$", amount) is None,
             "Incorrect amount value. It must be positive integer or float value"],
            [input_currency == output_currency, "Input and output currencies are the same"]
        ]

        for x in errors:
            if x[0]:
                message = x[1]
                break

        if message:
            return JsonResponse({'error': message})

        try:
            # Parse currency
            input_currency = Currency.parse_currency(input_currency)
            output_currency = Currency.parse_currency(output_currency) \
                if output_currency else None


        except Currency.MultipleObjectsReturned:
            message = 'Selected symbol is used to define multiple currencies. Use currency code instead'
        except Currency.DoesNotExist:
            message = "Incorrect currency"

        if message:
            return JsonResponse({'error': message})

        amount = float(amount)

        # try:
        if output_currency:
            result = {output_currency.code: round(ExchangeRate.get_rate(input_currency, output_currency) * amount, 2)}
        else:
            result = {currency: round(rate * amount, 2) for currency, rate in
                      ExchangeRate.get_rates(input_currency).items()}

        # except:
        #     return JsonResponse({'error': 'Unknown error occurred. Please contact support'})

        return JsonResponse({
            'input': {
                'amount': amount,
                'currency': input_currency.code
            },
            'output': result
        }, json_dumps_params={'indent': 2})
