import requests

def get_rates(currency: str):
    url = f'https://api.vatcomply.com/rates?base={currency}'

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Error: {response.status_code}: {response.text}')