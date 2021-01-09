''' Made by Reza Rahemtola (https://rezarahemtola.com) '''

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from win10toast_persist import ToastNotifier  # Notifications module
import pathlib


currentPath = str(pathlib.Path(__file__).parent.absolute())  # Catching the current directory
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get('https://www.binance.com/en/pos')
time.sleep(1)  # Waiting for the page to load
driver.find_element_by_css_selector(".css-1r19zeh").click()  # Click on the expand stacking products button
time.sleep(1)  # Wait for loading


# Scroll the modal multiple times to load all the assets
for i in range(3):
    driver.execute_script("""document.getElementById('modal-scroller').scrollTop = document.getElementById('modal-scroller').scrollHeight;""")
    time.sleep(0.5)

# Catching names of the provided crypto for locked stacking
names = [name.text for name in driver.find_elements_by_css_selector("div#modal-scroller .css-1hm1xxl")]


# 30 days is selected by default, checking if it's available for each crypto and saving the result and the APY
available30 = [True if button.get_attribute("class") == "css-nwkj16" else False for button in driver.find_elements_by_css_selector("div#modal-scroller .css-1dmwl4e button")]
apy30 = [apy.text for apy in driver.find_elements_by_css_selector("div#modal-scroller .css-m25ijz")]


# Trigger a click on the 60 days button for every crypto
[button.click() for button in driver.find_elements_by_css_selector("div#modal-scroller .css-1pp7m4q button") if button.text == "60"]

# 60 days is selected, checking if it's available for each crypto and saving the result and the APY
available60 = [True if button.get_attribute("class") == "css-nwkj16" else False for button in driver.find_elements_by_css_selector("div#modal-scroller .css-1dmwl4e button")]
apy60 = [apy.text for apy in driver.find_elements_by_css_selector("div#modal-scroller .css-m25ijz")]


# Trigger a click on the 90 days button for every crypto
[button.click() for button in driver.find_elements_by_css_selector("div#modal-scroller .css-1pp7m4q button") if button.text == "90"]

# 90 days is selected, checking if it's available for each crypto and saving the result and the APY
available90 = [True if button.get_attribute("class") == "css-nwkj16" else False for button in driver.find_elements_by_css_selector("div#modal-scroller .css-1dmwl4e button")]
apy90 = [apy.text for apy in driver.find_elements_by_css_selector("div#modal-scroller .css-m25ijz")]

# Some crypto aren't available for 60 and/or 90 days, therefore their buttons were not clicked and the available state is the one of the previous period
# Looping through the period buttons container and changing incorrect values
i = 0
for row in driver.find_elements_by_css_selector("div#modal-scroller .css-1pp7m4q"):
    numberOfButtons = len(row.find_elements_by_tag_name("button"))
    if numberOfButtons == 1:
        # Only 30 days stacking is provided, changing values to False for 60 & 90 days
        available60[i], available90[i] = False, False
    elif numberOfButtons == 2:
        # Only 30 & 60 days stacking are provided, changing values to False for 90 days
        available90[i] = False
    i += 1

# We don't need Chrome anymore, closing it
driver.quit()


# Creating a temporary list of dictionaries with 30, 60 and 90 days availability and the corresponding APY
temp = [{"30": (isAvailable30, apy30), "60": (isAvailable60, apy60), "90": (isAvailable90, apy90)} for isAvailable30, isAvailable60, isAvailable90, apy30, apy60, apy90 in list(zip(available30, available60, available90, apy30, apy60, apy90))]

# Associate token names with the corresponding availability and APY dictionnary
result = {key:value for key, value in list(zip(names, temp))}


# Initializing the notifier object
toaster = ToastNotifier()


# Open the watchlist file
with open(currentPath+"/watchlist.txt", "r") as file:
    for line in file:
        name, period = line.split()
        if result[name][period][0]:
            # Crypto asked in watchlist is available for the asked period, display a notification
            toaster.show_toast("Binance Locked Stacking", f"{name} stacking for {period} days with a {result[name][period][1]} APY is available !", icon_path=currentPath+"/Binance.ico", duration=None)
