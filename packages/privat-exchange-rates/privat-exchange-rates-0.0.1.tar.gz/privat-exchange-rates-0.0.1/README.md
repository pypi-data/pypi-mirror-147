![PyPI - Downloads](https://img.shields.io/pypi/dm/privat_exchange_rates?style=for-the-badge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/privat_exchange_rates?style=for-the-badge)

**Official Repo:** https://github.com/ValentynKhoroshchak/privat-exchange-rates

It uses the following libraries:

- [Requests](https://pypi.org/project/requests/) for requests to exchanges

# Quick Install / Usage

```bash
pip install privat_exchange_rates
```

```python
from datetime import datetime

from privat_exchange_rates import get_exchange_rates


def main():
    exchange_rates = get_exchange_rates(datetime(day=21, month=4, year=2022))

    print(exchange_rates)
    # {
    #     'date': '21.04.2022',
    #     'bank': 'PB',
    #     'baseCurrency': 980,
    #     'baseCurrencyLit': 'UAH',
    #     'exchangeRate': [{
    #         "baseCurrency": "UAH",
    #         "currency": "AUD",
    #         "saleRateNB": 12.8319250,
    #         "purchaseRateNB": 12.8319250
    #     }]
    # }
```