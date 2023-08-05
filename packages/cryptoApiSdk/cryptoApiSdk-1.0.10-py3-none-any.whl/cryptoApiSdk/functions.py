
import requests

BASE_URL = 'https://cdt2ogqvs5.execute-api.us-east-1.amazonaws.com/dev'

def get_coin_data(ticker: str):
    
    return requests.get(f'{BASE_URL}/{ticker}')
