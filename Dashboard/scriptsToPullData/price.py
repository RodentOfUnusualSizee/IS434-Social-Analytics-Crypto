import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Install driver
opts=webdriver.ChromeOptions()
opts.headless=True

driver = webdriver.Chrome(ChromeDriverManager().install() ,options=opts)

search_url = "https://www.investing.com/crypto/{}"

'''
Search params for crypto currencies
AAVE = aave/historical-data
Curve Finance = curve-dao-token/crv-usd-historical-data
Compound = compound/comp-usd-historical-data
Uniswap = uniswap/unis-usd-historical-data
Sushiswap = sushiswap/sushi-usd-historical-data
Maker = maker/mkr-usd-historical-data
'''

dict = {
    'AAVE': 'aave/historical-data',
    'Curve Finance': 'curve-dao-token/crv-usd-historical-data',
    'Compound': 'compound/comp-usd-historical-data',
    'Uniswap': 'uniswap/unis-usd-historical-data',
    'Sushiswap': 'sushiswap/sushi-usd-historical-data',
    'Maker': 'maker/mkr-usd-historical-data'
}

def getPrice(crypto,startDate,endDate):
    driver.get(search_url.format(dict[crypto]))

    driver.maximize_window()
    
    editDate(startDate, endDate)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "curr_table")))

    table_id = driver.find_element(By.ID,"curr_table") 
    body = table_id.find_element(By.TAG_NAME,"tbody")
    rows = body.find_elements(By.TAG_NAME,"tr")
    priceData = pd.DataFrame(columns=["Date", "Price", "Open", "High", "Low", "Vol.","Change %"])
    for row in rows:
        date = row.find_elements(By.TAG_NAME,"td")[0]
        print(date)
        price = row.find_elements(By.TAG_NAME,"td")[1]
        open = row.find_elements(By.TAG_NAME,"td")[2]
        high = row.find_elements(By.TAG_NAME,"td")[3]
        low = row.find_elements(By.TAG_NAME,"td")[4]
        vol = row.find_elements(By.TAG_NAME,"td")[5]
        change = row.find_elements(By.TAG_NAME,"td")[6]
        priceData = priceData.append({"Date":date.text, "Price":price.text, "Open":open.text, "High":high.text, "Low":low.text, "Vol":vol.text, "Change %":change.text}, ignore_index=True)

    #convert to csv
    priceData.to_csv("./priceData/{}_price_data.csv".format(crypto))

    driver.quit()

def editDate(startDate, endDate):
    widgetButton = driver.find_element(By.ID,'widgetFieldDateRange')
    driver.execute_script("arguments[0].click();", widgetButton)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "startDate")))
    #startdate
    sd = driver.find_element(By.ID,"startDate")
    sd.clear()
    sd.send_keys(startDate)
    #enddate
    ed = driver.find_element(By.ID,"endDate")
    ed.clear()
    ed.send_keys(endDate)
    #apply
    applyButton = driver.find_element(By.ID,'applyBtn')
    driver.execute_script("arguments[0].click();", applyButton)

getPrice("AAVE", "01/01/2021", "01/31/2021")