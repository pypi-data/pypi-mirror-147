from datetime import datetime

import requests

BANK_API_URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'


def get_exchange_rates(date: datetime) -> dict:
    """Get information on cash exchange rates of PrivatBank and the NBU on the selected date.

        Example:
             >>> get_exchange_rates(datetime(day=21, month=4, year=2022)

        Args:
          date: Selected date exchange rates,

        Returns:
          Exchange rates.
    """
    formatted_date = date.strftime("%d.%m.%Y")  # "21.04.2022" (day.month.year)
    response = requests.get(BANK_API_URL.format(date=formatted_date))

    return response.json()
