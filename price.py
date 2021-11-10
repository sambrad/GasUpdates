import requests
import config

data = []

def fetch_data():
    query = {'module':'stats', 'action':'ethprice','apikey':config.etherscan_apiKey}
    response = requests.get('https://api.etherscan.io/api', params=query)

    jsonresponse = response.json()

    result = jsonresponse["result"]

    eth_btc = result["ethbtc"]
    eth_btc_timestamp = result["ethbtc_timestamp"]
    eth_usd = result["ethusd"]
    eth_usd_timestamp = result["ethusd_timestamp"]

    global data
    data = [eth_btc, eth_btc_timestamp, eth_usd, eth_usd_timestamp]

def fetch_ethusd():
    fetch_data()
    global data
    return data[2]

def fetch_ethbtc():
    fetch_data()
    global data
    return data[0]

def fetch_ethusd_timestamp():
    fetch_data()
    global data
    return data[3]

def fetch_ethbtc_timestamp():
    fetch_data()
    global data
    return data[1]
