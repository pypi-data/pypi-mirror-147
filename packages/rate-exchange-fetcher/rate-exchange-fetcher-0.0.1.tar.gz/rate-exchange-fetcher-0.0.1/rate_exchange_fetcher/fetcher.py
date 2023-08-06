from rate_exchange_fetcher import client

def fetch_rate(from: str, to: str) -> float:
    response = client.get_rates(from)

    if to not in response['rates'].keys():
        raise ValueError(f'{to} is not a valid currency')
    
    return response['rates'][to]