import requests
import json
import time
import math
import price
import config
from datetime import datetime

hist = dict()

def get_input():
    print("Enter the length of session (minutes):")
    while True:
        try:
            session_len = int(input()) * 6
            break
        except ValueError:
            print("Please enter an integer") # T1 Error Log
    # Retrieving gwei threshold
    print("Enter your gwei threshold (int):")
    while True:
        try:
            gwei_thresh = int(input())
            break
        except ValueError:
            print("Please enter an integer") # T1 Error Log
    return session_len, gwei_thresh

def fetch_data(count, thresh_gwei):
    query = {'module':'gastracker', 'action':'gasoracle','apikey':config.etherscan_apiKey}
    response = requests.get('https://api.etherscan.io/api', params=query)

    jsonresponse = response.json()

    results = jsonresponse["result"]

    if (results == 'Invalid API Key'):
        print_error(results)
        quit()
    else:
        low_gwei = results["SafeGasPrice"]
        avg_gwei = results["ProposeGasPrice"]
        high_gwei = results["FastGasPrice"]
        last_ethusd = price.fetch_ethusd()
        add_hist(count, thresh_gwei, [datetime.now(), int(low_gwei), int(avg_gwei), int(high_gwei), float(last_ethusd)])

def add_hist(count, thresh_gwei, data):
    if len(hist) == 0:
        hist[1] = data
    else:
        hist[len(hist)+1] = data
    print_output(count, thresh_gwei, hist)

def print_output(count, thresh_gwei, hist):
    template = '{:^8} | {:^13} | {:^14} | {:^13} | {:^14} | {:^13} | {:^14} | {:^13} | {:^14}'

    latest_data = hist[len(hist)]
    last_time = latest_data[0]
    last_low = latest_data[1]
    last_avg = latest_data[2]
    last_high = latest_data[3]
    last_ethusd = latest_data[4]

    if (count > 0): # What if here we use a mod, which will allow the headers to show once again after certain point?
        s_latest_data = hist[len(hist)-1]
        s_last_low = s_latest_data[1]
        s_last_avg = s_latest_data[2]
        s_last_high = s_latest_data[3]
        s_last_ethusd = s_latest_data[4]
        dif_low = (last_low - s_last_low) / last_low
        dif_avg = (last_avg - s_last_avg) / last_avg
        dif_high = (last_high - s_last_high) / last_high
        dif_ethusd = (last_ethusd - s_last_ethusd) / last_ethusd
        str_dif_low = "{:.2%}".format(dif_low)
        str_dif_avg = "{:.2%}".format(dif_avg)
        str_dif_high = "{:.2%}".format(dif_high)
        str_dif_ethusd = "{:.2%}".format(dif_ethusd)
        if (dif_low > 0):
            str_dif_low = "+" + str_dif_low
        if (dif_avg > 0):
            str_dif_avg = "+" + str_dif_avg
        if (dif_high > 0):
            str_dif_high = "+" + str_dif_high
        if (dif_ethusd > 0):
            str_dif_ethusd = "+" + str_dif_ethusd
        if (last_low < thresh_gwei):
            print("\t**********************************************")
            print(template.replace(':', ':-').format('', '', '', '', '', '', '', '', ''))
            print(template.format(last_time.strftime("%H:%M:%S"), last_low, str_dif_low, last_avg, str_dif_avg, last_high, str_dif_high, last_ethusd, str_dif_ethusd))
            print("\t**********************************************")
            # Send text message
        else:
            print(template.replace(':', ':-').format('', '', '', '', '', '', '', '', ''))
            print(template.format(last_time.strftime("%H:%M:%S"), last_low, str_dif_low, last_avg, str_dif_avg, last_high, str_dif_high, last_ethusd, str_dif_ethusd))
    else:
        print()
        print("-----------------------------------------------------------------------------------------------------------")
        print("| Starting...                                              built by: sbrad.eth - donations appreciated :) |")
        print("-----------------------------------------------------------------------------------------------------------")
        print()
        print(template.format('Time', 'Safe Gwei', 'Safe Change', 'Prospose Gwei', 'Propose Change', 'Fast Gwei', 'Fast Change', 'ETH/USD', 'ETH/USD Change'))
        print(template.replace(':', ':-').format('', '', '', '', '', '', '', '', ''))
        print(template.format(last_time.strftime("%H:%M:%S"), last_low, '0.00%', last_avg, '0.00%', last_high, '0.00%', last_ethusd, '0.00%'))

def print_error(error):
    if (error == 'Invalid API Key'):
        print('----------------------------')
        print('Invalid API Key')
        print('----------------------------')
    else:
        print('error')
    # look into other errors that could occur

def get_min():
    min = 100000000
    for x in hist:
        x_data = hist[x]
        if x_data[1] < min:
            min = x_data[1]
            min_timestamp = x_data[0]
    return min, min_timestamp

def get_max():
    max = 0
    for x in hist:
        x_data = hist[x]
        if x_data[3] > max:
            max = x_data[3]
            max_timestamp = x_data[0]
    return max, max_timestamp

def perform_stats():
    session_low = get_min()
    session_high = get_max()
    print("Session Low: " + str(session_low[0]) + " at " + str(session_low[1]))
    print("Session High: " + str(session_high[0]) + " at " + str(session_high[1]))
    # stdev
    # other stats

def end():
    print()
    print()
    perform_stats()
    print()
    print("---------END---------")

def start():
    count = 0
    input = get_input()
    session_len = input[0]
    thresh_gwei = input[1]
    while (count < session_len):
        fetch_data(count, thresh_gwei)
        count += 1
        if (count != session_len):
            time.sleep(10.0)
    end()

start()
