# Currency converter API and CLI client
[![Build Status](https://travis-ci.org/ApaDoctor/currency_converter.svg?branch=master)](https://travis-ci.org/ApaDoctor/currency_converter) [![BCH compliance](https://bettercodehub.com/edge/badge/ApaDoctor/currency_converter?branch=master)](https://bettercodehub.com/)
## Run
There are Docker containers in the project.
If you want to create it and run following command:
```
docker-compose up --build -d
```



To fill data in database you can use this command:
```
python manage.py update_rates
```
This command create currencies if there are no them in database.
And then it replaces all exchange rates with actual.


## Admin panel
There is admin panel available in the project.
To access admin panel you need to have superuser account.
It can be created with the following command:
```
python manage.py createsuperuser
```

### Documentation
There is documentation available in the project.
You can access it with link in the admin or with the following link:
```
/admin/doc/models/
```

## Data update
Exchange rates change very quick. So good currency converter should update rates
At least once per day.

Now there are two update providers in this project:
- [RatesAPI](http://ratesapi.io)
- [ExchangeRatesAPI](http://api.exchangeratesapi.io)

They are free and have only 35 currencies with exchange rates.
By default is used RatesAPI.
You can change it in *currency_converter/settings.py*.
```
EXCHANGE_RATE_PROVIDER = 'ratesapi'
```

Also you can add your own exchange rate provider in these steps:
1. Implement method for RateProvider class located in *api/rate_provider.py*
   The name of the method must be protected(with underscore) _method_name.
   It must take currency code for which it will give the rates.
   Output is dict of rates.
   Where keys are 3-character length currency codes.
   And values are floats or integers with current exchange rates.
2. Register the method in RateProvider.ACTIVE_PROVIDERS.
   Put the name of the method without underscore.

### Actualize Rates
To actualize rates on production - use cron and choose your update frequency

## Examples

#### CLI
```
./currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
{   
    "input": {
        "amount": 100.0,
        "currency": "EUR"
    },
    "output": {
        "CZK": 2707.36, 
    }
}
```
```
./currency_converter.py --amount 0.9 --input_currency ¥ --output_currency AUD
{   
    "input": {
        "amount": 0.9,
        "currency": "CNY"
    },
    "output": {
        "AUD": 0.20, 
    }
}
```
```
./currency_converter.py --amount 10.92 --input_currency £ 
{
    "input": {
        "amount": 10.92,
        "currency": "GBP"
    },
    "output": {
        "EUR": 14.95,
        "USD": 17.05,
        "CZK": 404.82,
        .
        .
        .
    }
}
```

#### API
```
GET /currency_converter?amount=0.9&input_currency=¥&output_currency=AUD HTTP/1.1
{   
    "input": {
        "amount": 0.9,
        "currency": "CNY"
    },
    "output": {
        "AUD": 0.20, 
    }
}
```

```
GET /currency_converter?amount=10.92&input_currency=£ HTTP/1.1
{
    "input": {
        "amount": 10.92,
        "currency": "GBP"
    },
    "output": {
        "EUR": 14.95,
        "USD": 17.05,
        "CZK": 404.82,
        .
        .
        .
    }
}
```

