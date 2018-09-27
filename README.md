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


## Documentation
There are documentation available in the project:
```
/admin/doc/models/
```
You need to have account to access it.
It can be created with command:

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


### Examples

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

