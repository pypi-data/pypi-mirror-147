from rate_exchange_fetcher import client

def fetch_rate(from_currency: str, to_currency: str) -> float:
    response = client.get_rates(from_currency)

    if to not in response['rates'].keys():
        raise ValueError(f'{to_currency} is not a valid currency')
    
    return response['rates'][to_currency]