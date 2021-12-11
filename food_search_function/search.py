from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep

# create object for chrome options
chrome_options = Options()
base_url = 'https://www.fairprice.com.sg/search?query=potato'
# set chrome driver options to disable any popup's from the website
# to find local path for chrome profile, open chrome browser
# and in the address bar type, "chrome://version"
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('user-data-dir=C:\\Users\\Emily\\AppData\\Local\\Google\\Chrome\\User Data')
# To disable the message, "Chrome is being controlled by automated test software"
chrome_options.add_argument("disable-infobars")
# Pass the argument 1 to allow and 2 to block
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2
    })
# invoke the webdriver
# s=Service('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
browser = webdriver.Chrome('C:\\Users\\Emily\\Downloads\\chromedriver_win32\\chromedriver.exe')
browser.get(base_url)
delay = 5 #seconds


# declare empty lists
item_image, item_name, item_price = [],[],[]

while True:
    try:
        WebDriverWait(browser, delay)
        print ("Page is ready")
        sleep(5)
        html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        #print(html)
        soup = BeautifulSoup(html, "html.parser")

        # find_all() returns an array of elements.
        # We have to go through all of them and select that one you are need. And than call get_text()
        ingredient = soup.find_all('div', class_='sc-1plwklf-0 iknXK product-container')[0]
        # print(ingredient.get_text())
        image = ingredient.find('img', class_='sc-1ha5r19-0 ea-dTNP').get('src')
        name = ingredient.find('span', class_='sc-1bsd7ul-1 gGWxuk').get_text()
        price = ingredient.find('span', class_='sc-1bsd7ul-1 gJhHzP').get_text()
        item_image.append(image)
        item_name.append(name)
        item_price.append(price)


        break # it will break from the loop once the specific element will be present.
    except TimeoutException:
        print ("Loading took too much time!-Try again")

rows = zip(item_image, item_name, item_price)
import csv
newFilePath = 'shopee_item_list.csv'
with open(newFilePath, "w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
# close the automated browser
browser.close()

# class="sc-1plwklf-0 iknXK product-container"
# name ==> <div class="sc-1plwklf-7 jibnUN">
# image ==> <div class="sc-1plwklf-4 eSEyPy">
# price ==> <span class="sc-1bsd7ul-1 gJhHzP">