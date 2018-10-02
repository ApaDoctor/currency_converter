
def convert_currency(rates, amount):
    return {currency: round(rate * amount, 2) for currency, rate in rates.items()}
