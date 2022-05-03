from calendar import month
import os
from tracemalloc import start
import pandas as pd
from datetime import date
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Install driver
opts=webdriver.ChromeOptions()
opts.headless=True
#no sandbox mode
opts.add_argument("--no-sandbox")

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
    'Curve': 'curve-dao-token/crv-usd-historical-data',
    'Aave': 'aave/historical-data',
    'Compound': 'compound/comp-usd-historical-data',
    'Uniswap': 'uniswap/unis-usd-historical-data',
    'Sushiswap': 'sushiswap/sushi-usd-historical-data',
    'Maker': 'maker/mkr-usd-historical-data'
}

monthDict = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}

def getPrice(crypto):
    url = search_url.format(dict[crypto])
    WebDriverWait(driver, 15).until(EC.url_changes(url))
    
    driver.get(url)

    driver.maximize_window()

    startDate, endDate, path = dateFinder(crypto.lower())
    print(startDate)
    print(endDate)

    if startDate.split('/')[1] > endDate.split('/')[1]:
        print("No new data")
        return
    
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

    #format price to remove ,
    priceData['Price'] = priceData['Price'].str.replace(',','')
    # get old data
    oldData = pd.read_csv(path)
    #merge old data with new data
    newData = pd.concat([priceData, oldData])
    # convert to csv
    newData.to_csv(os.path.join(os.path.dirname(__file__),"../priceData/{}_price_data.csv".format(crypto.lower())))

    return "Success"

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


def dateFinder(crypto):
    string = crypto.split(" ")[0] + "_price_data.csv"
    print(string)
    path = "../priceData/" + string
    if os.access(path, os.F_OK):
        #startdate from first line csv
        startDate = pd.read_csv(path, nrows=1)['Date'].values[0]
        #format StartDate
        startDate = startDate.split(' ')
        startDate = monthDict[startDate[0]] + '/' + (str(int(startDate[1].strip(',')) + 1)) + '/' + startDate[2]
        #endDate is current date
        endDate = date.today().strftime("%m/%d/%Y")
        endDate = endDate.split('/')
        endDate = endDate[0] + '/' + str(endDate[1]).replace('0','') + '/' + endDate[2]
        return '01/01/2021', endDate, path
    else:
        #default value
        startDate = "01/01/2021"
        
        #endDate is current date
        endDate = date.today().strftime("%m/%d/%Y")

        return startDate, endDate, path

def initial():
    for key in dict:
        getPrice(key)
        time.sleep(3)
    # getPrice('Curve')


initial()

