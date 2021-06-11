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

import matplotlib.pyplot as plt
import numpy as np

import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler 

my_token = '1234'
chat_id = 1234


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


    with open('C:/Users/james/Desktop/test_file/test.txt', 'wb') as f:
        pickle.dump(data_list, f)

def draw_graph() :
    with open('C:/Users/james/Desktop/test_file/test.txt', 'rb') as f:
        data = pickle.load(f)
        ksp_orc_fluc = data["ksp_orc"]
        klay_orc_fluc = data["klay_orc"]
        bnb_belt_fluc = data["bnb_belt"]
        month = data["month"]
        day = data["day"]

    label_list = []
    i = 0
    for i in range(len(month)) :
        if month[i] != None:
            label = month[i] + '/' + day[i]
            label_list.append(label)
        else :
            label_list.append(None)

    ytick_list = []
    y = -100
    while y < 101 :
        ytick_list.append(y)
        y += 10

    plot_x = np.arange(672)

    plt.plot(plot_x, ksp_orc_fluc, color="#f39755", label='ksp_orc') # ksp_orc
    plt.plot(plot_x, klay_orc_fluc, color='#6f6558', label='klay_orc') # klay_orc
    plt.plot(plot_x, bnb_belt_fluc, color='#fdd493', label='bnb_belt') # bnb_belt

    plt.xlabel('date', fontsize=12)
    plt.ylabel('fluc', fontsize=12)

    plt.xticks(plot_x, label_list, fontsize=12)
    plt.yticks(np.arange(-100, 110, 10), ytick_list, fontsize=12)

    # plt.legend(loc='best', fontsize=9)

    plt.tick_params(axis='x', direction='in', length=3, pad=6, top=True)

    plt.savefig('C:/Users/james/Desktop/test_file/save_graph.png', facecolor='#eeeeee', dpi = 200)
    print("draw")

def write_file() :
    ksp_orc = 5.3
    klay_orc = -22
    bnb_belt = -42
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

    with open('C:/Users/james/Desktop/test_file/test.txt', 'rb') as f:
        data = pickle.load(f)
        del data["ksp_orc"][0]
        del data["klay_orc"][0]
        del data["bnb_belt"][0]
        del data["month"][0]
        del data["day"][0]

    with open('C:/Users/james/Desktop/test_file/test.txt', 'wb') as f:
        # 최근 데이터
        data["ksp_orc"].append(ksp_orc)
        data["klay_orc"].append(klay_orc)
        data["bnb_belt"].append(bnb_belt)
        data["month"].append(month)
        data["day"].append(day)
        pickle.dump(data, f)

def remove_png_file() :
    file = 'C:/Users/james/Desktop/test_file/save_graph.png'

    if os.path.isfile(file):
        os.remove(file)

def draw_graph_func() :
    draw_graph()

def crawling_bnb_belt():
    bnb_rateURL = 'https://www.coingecko.com/ko/%EC%BD%94%EC%9D%B8/belt'

    bnb_rate_result = requests.get(bnb_rateURL)

    bnb_rate_soup = BeautifulSoup(bnb_rate_result.text, "html.parser")
    
    temp_list = []
    
    belt_rate = bnb_rate_soup.find("div", {"class": 'text-muted'})
    for rate in belt_rate.find_all('div') :
        index = float(rate.text[:11])
        temp_list.append(index)

    bnb_belt_index = temp_list[1] # 현재 rate
    bnb_belt_index_past = 0.1339 # 리밸런싱 시점-----------------------------------------------------------------------------------------------------------

    bnb_belt_fluc = bnb_belt_index - bnb_belt_index_past
    bnb_belt_fluc = bnb_belt_fluc / bnb_belt_index_past
    bnb_belt_fluc = round(bnb_belt_fluc * 100, 2)

    bnb_belt_index = round(bnb_belt_index, 4)
    bnb_belt_index_past = round(bnb_belt_index_past, 4)

    if bnb_belt_fluc < 0:
        memo = "(belt 가치- 개수+)"
    elif bnb_belt_fluc == 0:
        memo = "(변동 없음)"
    else :
        memo = "(belt 가치+ 개수-)"

    sending_text = "bnb-belt 스왑비(예치시점): " + str(bnb_belt_index_past) + "bnb\n"
    sending_text2 = "bnb-belt 스왑비(현재): " + str(bnb_belt_index) + "bnb\n"
    sending_text3 = "bnb-belt 스왑비 변동률: " + str(bnb_belt_fluc) + "%" + memo + "\n"

    bnb_belt_fluc = float(bnb_belt_fluc)

    return sending_text + sending_text2 + sending_text3, bnb_belt_fluc

text = crawling_bnb_belt()
print(text)

# write_file()

# draw_graph()

# remove_png_file()


# scheduler1 = schedule.Scheduler()
# scheduler1.every(10).seconds.do(draw_graph_func)

# while True:
#     scheduler1.run_pending()
#     time.sleep(1)

# bot = telegram.Bot(token=my_token)
# # message reply function
# def get_message(update, context) :
#     update.message.reply_text("got text")
#     update.message.reply_text(update.message.text)


# # rate reply function
# def get_graph_image(update, context) :
#     update.message.reply_text("잠시만 기다려 주세요!")
#     draw_graph()
#     bot.sendPhoto(chat_id=chat_id, photo=open('C:/Users/james/Desktop/test_file/save_graph.png', 'rb'))
#     remove_png_file()

# updater = Updater(my_token, use_context=True)

# message_handler = MessageHandler(Filters.text & (~Filters.command), get_message) # 메세지중에서 command 제외
# updater.dispatcher.add_handler(message_handler)

# keth_rate_handler = CommandHandler('test', get_graph_image)
# updater.dispatcher.add_handler(keth_rate_handler)

# updater.start_polling(timeout=3, clean=True)
# updater.idle()