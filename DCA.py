from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time as t
import csv

#some not actual TICKER symbols
Current_Holdings=["JPM","NVDA","DIS","AT&","MSFT","PEP","JNJ"]
amount =input("How much would you like to dollar cost average this month?")

#retrieve login info from file
with open("c:/Users/tyler/OneDrive/Documents/Python_Scripts/Login.txt" ,"r") as login:
    user = login.readline()
    passwd = login.readline()


driver = webdriver.Chrome('c:/Users/tyler/OneDrive/Documents/Python_Scripts/chromedriver')
driver.get('https://www.schwab.com/public/schwab/nn/login/login.html&lang=en')
driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
t.sleep(1.5)

#identify locations                       
username = driver.find_element_by_xpath('//*[@id="LoginId"]')
password = driver.find_element_by_xpath('//*[@id="Password"]')


#fill in password
password.send_keys(passwd)
t.sleep(2.0)

#user
username.send_keys(user)
t.sleep(3.0)

##For some reason after inputting user it automatically submits (without login.click()) ???


## Dollar cost averaging - select from list of holdings to average into

history = driver.find_element_by_link_text("Trade")
history.click()
t.sleep(2.0)
# driver.get("https://client.schwab.com/secure/cc/accounts/historynew")

slices = driver.find_element_by_partial_link_text("Schwab Stock Slices")
slices.click()
t.sleep(3.0)

driver.find_element_by_id("modalClose").click()


t.sleep(1.5)
searchbar = driver.find_element_by_id("symbolSearchInput")
for stock in Current_Holdings:
    erase=0
    while erase<4:
        searchbar.send_keys(Keys.BACKSPACE)
        erase+=1
    searchbar.send_keys(stock)
    t.sleep(0.5)
    searchbar.send_keys(Keys.ENTER)
    value = "select-" + str(stock)
    if stock!="AT&":
        first = driver.find_element_by_id(value)
    else:
        first = driver.find_element_by_id("select-"+"T")
    actions = ActionChains(driver)
    actions.move_to_element(first).perform()
    driver.execute_script("arguments[0].click();", first)
    
step = driver.find_element_by_id("continue")
actions = ActionChains(driver)
actions.move_to_element(step).perform()
driver.execute_script("arguments[0].click();", step)


t.sleep(3.0)
driver.find_element_by_id("investAmt").send_keys(amount)

driver.find_element_by_class_name('account-selector-button').click()
t.sleep(1.2)
driver.find_element_by_link_text('Individual').click()
t.sleep(1.35)
driver.find_element_by_xpath('//button[text()="Review Your Selection"]').click()
t.sleep(10.0)
driver.quit()