import telegram
#from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules
import requests
from bs4 import BeautifulSoup
import schedule
import time
import pickle
import json
import urllib.request
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

my_token = '1234'
chat_id = 1234

# 리밸런싱 시점
orc_swap_rate = 19.0564 #ksp-orc
klay_orc_swap_rate = 0.978 #klay-orc
bnb_belt_index_past = 0.1339 #bnb-belt

options = Options()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


def il_calculator(fluc) : # input type : str, return type : str
    driver = webdriver.Chrome('/home/ubuntu/chromedriver', chrome_options=options)
    URL = 'https://coinmarketcap.com/ko/yield-farming/'
    driver.get(URL)
    driver.implicitly_wait(time_to_wait=3)
    driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div/div[3]/div[3]/span/div/button').click()
    input_fluc = driver.find_element_by_class_name('cxm5lu-0')
    time.sleep(1)
    input_fluc.send_keys(fluc)
    time.sleep(1)
    il = driver.find_element_by_class_name('imLApL').text

    driver.close()
    return il

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

    
def crawling_klay_ksp():
    klay_price = crawling_klay_price()
    ksp_price = crawling_ksp_price()
    
    ksp_value_rate = klay_price / ksp_price #현재
    ksp_swap_rate = 0.0977 #리밸런싱 시점-----------------------------------------------------------------------------------------------------------

    ksp_fluc = ksp_value_rate - ksp_swap_rate
    ksp_fluc = ksp_fluc / ksp_swap_rate
    ksp_fluc = round(ksp_fluc * 100, 2)

    ksp_value_rate = round(ksp_value_rate, 4)
    ksp_swap_rate = round(ksp_swap_rate, 4)

    if ksp_fluc < 0:
        memo = "(klay 가치- 개수+)"
    elif ksp_fluc == 0:
        memo = "(변동 없음)"
    else :
        memo = "(klay 가치+ 개수-)"

    sending_text = "ksp 스왑비(예치시점): " + str(ksp_swap_rate) + "ksp\n"
    sending_text2 = "ksp 스왑비(현재): " + str(ksp_value_rate) + "ksp\n"
    sending_text3 = "ksp 스왑비 변동률: " + str(ksp_fluc) + "%" + memo + "\n"

    return sending_text + sending_text2 + sending_text3

def crawling_klay_orc():
    klay_price = crawling_klay_price()
    orc_price = crawling_orc_price()
    
    orc_value_rate = klay_price / orc_price #현재

    orc_fluc = orc_value_rate - klay_orc_swap_rate
    orc_fluc = orc_fluc / klay_orc_swap_rate
    orc_fluc = round(orc_fluc * 100, 2)
    orc_fluc_calc = str(abs(orc_fluc))

    orc_value_rate = round(orc_value_rate, 4)

    il_data = il_calculator(orc_fluc_calc)

    if orc_fluc < 0:
        memo = "(klay 가치- 개수+)"
    elif orc_fluc == 0:
        memo = "(변동 없음)"
    else :
        memo = "(klay 가치+ 개수-)"

    sending_text = "klay-orc 스왑비(예치시점): " + str(klay_orc_swap_rate) + "orc\n"
    sending_text2 = "klay-orc 스왑비(현재): " + str(orc_value_rate) + "orc\n"
    sending_text3 = "klay-orc 스왑비 변동률: " + str(orc_fluc) + "%" + memo + "\n"
    sending_text4 = '비영구적 손실: ' + il_data + '\n'

    orc_fluc = float(orc_fluc)

    return sending_text + sending_text2 + sending_text3 + sending_text4, orc_fluc

def crawling_ksp_orc():
    ksp_price = crawling_ksp_price()
    orc_price = crawling_orc_price()
    
    orc_value_rate = ksp_price / orc_price #현재

    orc_fluc = orc_value_rate - orc_swap_rate
    orc_fluc = orc_fluc / orc_swap_rate
    orc_fluc = round(orc_fluc * 100, 2)
    orc_fluc_calc = str(abs(orc_fluc))

    orc_value_rate = round(orc_value_rate, 4)

    il_data = il_calculator(orc_fluc_calc)

    if orc_fluc < 0:
        memo = "(ksp 가치- 개수+)"
    elif orc_fluc == 0:
        memo = "(변동 없음)"
    else :
        memo = "(ksp 가치+ 개수-)"

    sending_text = "ksp-orc 스왑비(예치시점): " + str(orc_swap_rate) + "orc\n"
    sending_text2 = "ksp-orc 스왑비(현재): " + str(orc_value_rate) + "orc\n"
    sending_text3 = "ksp-orc 스왑비 변동률: " + str(orc_fluc) + "%" + memo + "\n"
    sending_text4 = '비영구적 손실: ' + il_data + '\n'

    orc_fluc = float(orc_fluc)

    return sending_text + sending_text2 + sending_text3 + sending_text4, orc_fluc

def crawling_bnb_belt() :
    driver = webdriver.Chrome('/home/ubuntu/chromedriver', chrome_options=options)
    URL = 'https://exchange.pancakeswap.finance/#/swap'

    driver.get(URL)
    driver.implicitly_wait(time_to_wait=2)
    element = []
    element = driver.find_elements_by_xpath('//*[@id="pair"]')
    element[1].click()
    search = driver.find_element_by_xpath('//*[@id="token-search-input"]')
    search.send_keys('belt')
    time.sleep(1)
    search.send_keys(Keys.ENTER)
    time.sleep(1)
    input_belt = driver.find_element_by_xpath('//*[@id="swap-currency-output"]/div/div[2]/input')
    input_belt.send_keys('1')
    time.sleep(3)
    bnb_index = driver.find_element_by_xpath('//*[@id="swap-currency-input"]/div/div[2]/input').get_attribute("value") # belt 스왑비 type : str
    
    bnb_belt_index = float(bnb_index) #현재 rate

    bnb_belt_fluc = bnb_belt_index - bnb_belt_index_past
    bnb_belt_fluc = bnb_belt_fluc / bnb_belt_index_past
    bnb_belt_fluc = round(bnb_belt_fluc * 100, 2) 
    bnb_belt_fluc_calc = str(abs(bnb_belt_fluc)) #변동률 절대값

    bnb_belt_index = round(bnb_belt_index, 4)

    il_data = il_calculator(bnb_belt_fluc_calc)

    if bnb_belt_fluc < 0:
        memo = "(belt 가치- 개수+)"
    elif bnb_belt_fluc == 0:
        memo = "(변동 없음)"
    else :
        memo = "(belt 가치+ 개수-)"

    sending_text = "bnb-belt 스왑비(예치시점): " + str(bnb_belt_index_past) + "bnb\n"
    sending_text2 = "bnb-belt 스왑비(현재): " + str(bnb_belt_index) + "bnb\n"
    sending_text3 = "bnb-belt 스왑비 변동률: " + str(bnb_belt_fluc) + "%" + memo + "\n"
    sending_text4 = '비영구적 손실: ' + il_data + '\n'

    bnb_belt_fluc = float(bnb_belt_fluc)

    driver.close()
    return sending_text + sending_text2 + sending_text3 + sending_text4, bnb_belt_fluc

bot = telegram.Bot(token=my_token)

def sending_on_schedule():     #bot에 메세지 보내는 함수
    dotted_line = "------------------------------\n"
    sending_text3, ksp_orc = crawling_ksp_orc()
    sending_text, klay_orc = crawling_klay_orc()
    sending_text4, bnb_belt = crawling_bnb_belt()
    # sending_text5 = crawling_klay_ksp()
    text_sum = sending_text3 + dotted_line + sending_text + dotted_line + sending_text4 #+ dotted_line + sending_text5
    bot.sendMessage(chat_id=chat_id, text=text_sum)

    month = int(time.strftime('%m'))  # month
    day = int(time.strftime('%d'))  # day
    hour = int(time.strftime('%H'))
    minute = int(time.strftime('%M'))

    if hour == 0 and minute < 15 :
        month = str(month)
        slash = '/'
        day = str(day)
    else :
        month = None
        slash = None
        day = None

    with open('/home/ubuntu/important_data/data_fluc.txt', 'rb') as f:
        data = pickle.load(f)
        del data["ksp_orc"][0]
        del data["klay_orc"][0]
        del data["bnb_belt"][0]
        del data["month"][0]
        del data["day"][0]

    with open('/home/ubuntu/important_data/data_fluc.txt', 'wb') as f:
        # 최근 데이터
        data["ksp_orc"].append(ksp_orc)
        data["klay_orc"].append(klay_orc)
        data["bnb_belt"].append(bnb_belt)
        data["month"].append(month)
        data["day"].append(day)
        pickle.dump(data, f)




sending_on_schedule()
scheduler1 = schedule.Scheduler()
scheduler1.every(15).minutes.do(sending_on_schedule)

while True:
    scheduler1.run_pending()
    time.sleep(1)



