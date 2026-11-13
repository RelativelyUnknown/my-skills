import time


def fetch_rate(currency):
    return 1.0


_rates = {}


def exchange_rate(currency, now=time.monotonic, ttl=300):
    hit = _rates.get(currency)
    if hit and now() - hit[0] < ttl:
        return hit[1]
    value = fetch_rate(currency)
    _rates[currency] = (now(), value)
    return value
