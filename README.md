# BinanceLockedStakingCheck
A simple Python script which checks the availability of Binance's locked stacking products and display a notification if a wanted product is available.

Made for Windows but could be adapted to other OSs without major issues.

## Instructions
1. Install [Python](https://www.python.org/downloads/)
2. Download the version of [chromedriver.exe](https://chromedriver.chromium.org/downloads) that corresponds to your version of Chrome.
3. Edit the watchlist.txt file to match the products you want. You should put one request per line with the token name and the wanted period in days, separated by a space. You can take a look at the provided watchlist example.
4. All done ! You can now run the script when you want or create a scheduled task for full automation.
