import pickle
import requests
from bs4 import BeautifulSoup
import schedule
import time

import selenium
from selenium import webdriver

import json
import urllib.request
# from urllib.request import Request, urlopen
import os

def crawling_coinone() :
    urlTicker = urllib.request.urlopen('https://api.coinone.co.kr/ticker/?currency=all')
    readTicker = urlTicker.read()
    jsonTicker = json.loads(readTicker)
    Findklay = jsonTicker['klay']['last']
    Findorc = jsonTicker['orc']['last']
    Findksp = jsonTicker['ksp']['last']
    klay = float(Findklay)
    orc = float(Findorc)
    ksp = float(Findksp)

    print(klay)
    print(orc)
    print(ksp)

def write_data() :
    # 형식 : 페어, 월(자정기준), slash, 일(자정기준) 
    data_list = {"ksp_orc" : [],
                 "klay_orc" : [],
                 "bnb_belt" : [],
                 "month" : [],
                 "day" : [],
                 }


    for pair in range(672) :
        data_list["ksp_orc"].append(0)
        data_list["klay_orc"].append(0)
        data_list["bnb_belt"].append(0)
        data_list["month"].append(None)
        data_list["day"].append(None)


    with open('C:/Users/james/Desktop/test_file', 'wb') as f:
        pickle.dump(data_list, f)

write_data()

def crawling_test() :

    URL = 'https://scolkg.com/'

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(r'C:/Users/james/Desktop/chromedriver.exe', options=options)
    driver.get(url = URL)

    coinone = driver.find_element_by_xpath('//*[@id="app_coinfilter"]/div[2]/button[2]')
    coinone.click()
    search_box = driver.find_element_by_xpath('//*[@id="app_coinfilter"]/div[4]/input')
    search_box.send_keys('klay')
    klay_button = driver.find_element_by_xpath('//*[@id="app_coinfilter"]/div[5]/button[1]')
    klay_button.click()

    klay = driver.find_element_by_class_name('table').text
    print(klay)
    

    driver.close()

def crawling_test2() :
    
    URL = 'https://www.coingecko.com/ko/%EC%BD%94%EC%9D%B8/klaytn#markets'

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(r'C:/Users/james/Desktop/chromedriver.exe', options=options)

    driver.get(url = URL)
    coinone = driver.find_element_by_xpath('//*[@id="spot"]/div/div[1]/div[2]/table/tbody[2]/tr[14]/td[4]/div').text
    print(coinone)
    

    driver.close()



def crawling_klay_price():
    urlTicker = urllib.request.urlopen('https://api.coinone.co.kr/ticker/?currency=all')
    readTicker = urlTicker.read()
    jsonTicker = json.loads(readTicker)
    Findklay = jsonTicker['klay']['last']
    klay = float(Findklay)

    return klay

def crawling_orc_price():
    urlTicker = urllib.request.urlopen('https://api.coinone.co.kr/ticker/?currency=all')
    readTicker = urlTicker.read()
    jsonTicker = json.loads(readTicker)
    Findorc = jsonTicker['orc']['last']
    orc = float(Findorc)

    return orc

def crawling_ksp_price():
    urlTicker = urllib.request.urlopen('https://api.coinone.co.kr/ticker/?currency=all')
    readTicker = urlTicker.read()
    jsonTicker = json.loads(readTicker)
    Findksp = jsonTicker['ksp']['last']
    ksp = float(Findksp)

    return ksp






