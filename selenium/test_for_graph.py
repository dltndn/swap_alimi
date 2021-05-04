import telegram
#from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules
import requests
from bs4 import BeautifulSoup
import schedule
import time
import matplotlib.pyplot as plt
import numpy as np
import pickle

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
    bnb_belt_index_past = 0.1413 # 리밸런싱 시점-----------------------------------------------------------------------------------------------------------

    bnb_belt_fluc = bnb_belt_index - bnb_belt_index_past
    bnb_belt_fluc = bnb_belt_fluc / bnb_belt_index_past
    bnb_belt_fluc = round(bnb_belt_fluc * 100, 2) #return 값

    if bnb_belt_fluc < 0:
        memo = "(belt 가치- 개수+)"
    elif bnb_belt_fluc == 0:
        memo = "(변동 없음)"
    else :
        memo = "(belt 가치+ 개수-)"


    return bnb_belt_fluc

# index = crawling_bnb_belt()

def get_time() :
    print(time.strftime('%m'))  # month
    print(time.strftime('%d'))  # day
    print(time.strftime('%H')) 
    print(time.strftime('%M'))
    print(time.strftime('%S'))


def write_data() :
    # 형식 : 페어, 월(자정기준), 일(자정기준), 12(정오) 
    data_list = {"ksp_orc" : [],
                 "klay_orc" : [],
                 "bnb_belt" : [],
                 "month" : [],
                 "slash" : [],
                 "day" : [],
                 }

    for pair in range(672) :
        data_list["ksp_orc"].append(0)
        data_list["klay_orc"].append(0)
        data_list["bnb_belt"].append(0)
        data_list["month"].append(None)
        data_list["slash"].append(None)
        data_list["day"].append(None)

    with open('data_fluc.txt', 'wb') as f:
        pickle.dump(data_list, f)

    

def draw_graph() :
    with open('data_fluc.txt', 'rb') as f:
        data = pickle.load(f)
        ksp_orc_fluc = data["ksp_orc"]
        klay_orc_fluc = data["klay_orc"]
        bnb_belt_fluc = data["bnb_belt"]
        month = data["month"]
        slash = data["slash"]
        day = data["day"]

    xticks_index =np.arange(672)
    label_list = []

    i = 0
    for i in range(len(month)) :
        if month[i] != None:
            label = month + slash + day
            label_list.append(label)
        else :
            label_list.append(None)

    plot_x = np.arange(672)

    plt.plot(plot_x, ksp_orc_fluc, color="#f39755", label='ksp_orc') # ksp_orc
    plt.plot(plot_x, klay_orc_fluc, color='#6f6558', label='klay_orc') # klay_orc
    plt.plot(plot_x, bnb_belt_fluc, color='#fdd493', label='bnb_belt') # bnb_belt

    plt.xlabel('date')
    plt.ylabel('fluc')

    plt.xticks(plot_x, label_list)
    plt.yticks(np.arange(-100, 110, 10), ytick_list)

    plt.legend(loc='best', fontsize=10)

    plt.tick_params(axis='x', direction='in', length=3, pad=6, top=True)

    plt.show()


# label_list = []
# label_list2 = []

# i = 0
# for i in range(10) :
#     if i % 3 == 0 :
#         label_list.append("1")
#         label_list2.append("2")
#     elif i % 7 == 0:
#         label_list.append(None)
#         label_list2.append(None)
#     else :
#         label_list.append('7')
#         label_list2.append('8')

# label_list_test = []
# i = 0
# for i in range(len(label_list)) :
#     if label_list[i] == None:
#         label = None
#         label_list_test.append(label)
#     else :
#         label = label_list[i] + label_list2[i]
#         label_list_test.append(label)
#     print(label_list[i])

# x_index = np.arange(10)

# y_index = []

# i = 0
# for i in range(10) :
#     y = i -100
#     y_index.append(y)
#     i += 1

# plt.plot(x_index, y_index, label='ksp_orc')

# ytick_list = []
# y = -100
# i = 0
# while y < 101 :
#     ytick_list.append(y)
#     y += 10
#     i += 1
    
# plt.xlabel('date')
# plt.ylabel('fluc')

# plt.xticks(x_index, label_list_test)
# plt.yticks(np.arange(-100, 110, 10), ytick_list)

# plt.legend(loc='best', fontsize=9)

# plt.tick_params(axis='x', direction='in', length=3, pad=6, top=True)

# plt.show()

a = np.arange(10)
print(a)
print(a[8])
a[-2] = 21
print(a)
print(a[8])
