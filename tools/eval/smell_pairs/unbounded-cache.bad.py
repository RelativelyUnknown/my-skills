from functools import cache


@cache
def exchange_rate(currency):
    return fetch_rate(currency)
