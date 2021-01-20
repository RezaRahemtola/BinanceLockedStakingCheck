''' Made by Reza Rahemtola (https://rezarahemtola.com) '''

import json
import requests
from win10toast_persist import ToastNotifier  # Notifications module
import pathlib

currentPath = str(pathlib.Path(__file__).parent.absolute())  # Catching the current directory

# Requesting data from Binance
response = json.loads(requests.get("https://www.binance.com/gateway-api/v1/friendly/pos/union?pageSize=50&pageIndex=1&status=ALL").text)["data"]

result = []
for item in response:
    for asset in item["projects"]:
        if not asset["sellOut"]:
            # Asset available, adding a dictionary with asset name, duration and APY to the result list
            result.append({
                "asset": asset["asset"],
                "duration": asset["duration"],
                "APY": str(round(float(asset["config"]["annualInterestRate"])*100, 2))
            })


# Initializing the notifier object
toaster = ToastNotifier()

# Open the watchlist file
with open(currentPath+"/watchlist.txt", "r") as file:
    for line in file:
        name, period = line.split()
        for item in result:
            if name == item["asset"] and period == item["duration"]:
                # Crypto asked in watchlist is available for the asked period, display a notification
                toaster.show_toast("Binance Locked Stacking", f"{item['asset']} staking for {item['duration']} days with a {item['APY']}% APY is available !", icon_path=currentPath+"/Binance.ico", duration=None)
