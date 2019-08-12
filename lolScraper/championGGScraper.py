from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re
import json
import lxml
import pandas as pd
from pandas.io.json import json_normalize


browser = webdriver.Firefox(executable_path='/home/joshua/Downloads/geckodriver')
browser.get("https://champion.gg/statistics/?league=platinum")
timeout = 7
html_page = browser.page_source
browser.quit()

soup = BeautifulSoup(html_page, "lxml")
patternMatchup = re.compile(r"matchupData.stats\s+=\s+(\[.*?\])")
script = soup.find("script", text=patternMatchup)

patternChamps = re.compile(r"champData\s+=\s(\{.*?\})")
scriptChamps = soup.find("script", text=patternChamps)

champData = patternChamps.search(scriptChamps.text).group(1)
champData = json.loads(champData)
data = patternMatchup.search(script.text).group(1)
data = json.loads(data)
for i in data:
    for x in champData:
        if i['key'] == str(x):
            i['key'] = champData[x]
            print(i['key'])

data = json_normalize(data)
df = pd.DataFrame(data)
df.to_csv("platinumChampData.csv", index=False)

print(df)