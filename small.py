import requests
import json
import time
from datetime import datetime

# TODOs:
# T1-   Create Error log like a dict or something that has error value and message and have all errors uniform
# T2-   Perform statistics on the session
# T3-   Send text messages on low Gwei
# T4-   Send to PostgreSQL databse

def get_input():
    # Retrieving session length
    print("Enter the length of session (minutes):")
    len_input = input()
    while True:
        try:
            session_len = int(len_input) * 6
            break
        except:
            print("Please enter an integer") # T1 Error Log
    # Retrieving gwei threshold
    print("Enter your gwei threshold (int):")
    thresh_input = input()
    while True:
        try:
            gwei_thresh = int(thresh_input)
            break
        except:
            print("Please enter an integer") # T1 Error Log
    return session_len, gwei_thresh

def fetch_data(count, thresh_gwei):
    query = {'module':'gastracker', 'action':'gasoracle','apikey':'KIR251TFNBU29X9UKX4Y8Z7F5X924A381E'}
    response = requests.get('https://api.etherscan.io/api', params=query)
    # T1 Error Log
    # T4 PostgreSQL
    jsonresponse = response.json()
    results = jsonresponse["result"]
    low_gwei = results["SafeGasPrice"]

    print_output(count, low_gwei, thresh_gwei)

def print_output(count, gwei, thresh_gwei):
    template = '{:^8} | {:^3}'
    if count == 0:
        print(template.format('time', 'gwei'))
    if threshold(thresh_gwei, int(gwei)):
        # T3 Send text
        print("*****")
        print(gwei)
        print("*****")
    else:
        print(template.replace(':', ':-').format('', '', ''))
        print(template.format(datetime.now().strftime("%H:%M:%S"), gwei))

def threshold(thresh_gwei, cur_gwei):
    flag = False
    if cur_gwei <= thresh_gwei:
        flag = True
    return flag


# turn start into run() and have start for first 3 lines or so and then the rest named something else
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
    # T2 Stats

start()
