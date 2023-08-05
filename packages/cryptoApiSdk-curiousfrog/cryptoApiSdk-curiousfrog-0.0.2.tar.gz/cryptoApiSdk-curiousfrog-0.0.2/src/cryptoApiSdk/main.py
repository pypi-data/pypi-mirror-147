
import requests

BASE_URL = 'ec2-54-209-240-53.compute-1.amazonaws.com:8080/'

def get_coin_data(ticker: str):
    
    return requests.get(f'{BASE_URL}/{ticker}')

