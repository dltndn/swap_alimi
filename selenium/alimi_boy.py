import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules
import requests
from bs4 import BeautifulSoup
import schedule
import time

my_token = '55'
chat_id = 5


def crawling_keth():
    

    klayURL = 'https://coinmarketcap.com/ko/currencies/klaytn/'

    klay_result = requests.get(klayURL)

    temp_list_eth = []
    temp_list_rate = []
    temp_list_updown = []
    klay_soup = BeautifulSoup(klay_result.text, "html.parser")
    change_rate = klay_soup.find_all("p", {"class": "sc-10nusm4-0"})
    for rate in change_rate:
        eth_value = rate.text
        eth_value = eth_value[:9]
        temp_list_eth.append(eth_value)

        updown = rate.find("span", {"class": "gClTFY"})
        updown = updown.find("span")
        temp_list_updown.append(str(updown["class"]))

        rate_num = rate.find("span", {"class": "gClTFY"}).text
        rate_num = rate_num.replace("%", "")
        temp_list_rate.append(float(rate_num))
        
    updown_result = temp_list_updown[-1]
    if "up" in updown_result:
        symbol = "+"
    elif "down" in updown_result:
        symbol = "-"

    index = str(temp_list_rate[-1]) #최근 24시간 기준 변동률
    eth_value_rate = temp_list_eth[-1] #현재
    eth_swap_rate = 0.000862 #리밸런싱시점

    eth_value_rate = float(eth_value_rate)
    son = eth_value_rate - eth_swap_rate
    mom = eth_swap_rate
    cal_result = son / mom
    cal_result = cal_result * 100
    cal_result = round(cal_result, 2)

    if cal_result > 0:
        memo = "__일단 관망..."
        ass = "+"
    else :
        memo = "__클레이 리밸런싱 대기"
        ass = ""


    sending_text = "현재 klay-eth 변동률(최근 24시간 기준): " + symbol + index + "%" + "\n" 
    sending_text2 = "이더가치: " + str(eth_value_rate) + "eth" + "(현재)" + "\n"
    sending_text3 = "이더가치: " + str(eth_swap_rate) + "eth" + "(리밸런싱시점)" + "\n"
    sending_text4 = "스왑시점 대비 현재 가치 변동률: " + ass + str(cal_result) + "%" + memo
    return sending_text + sending_text2 + sending_text3 + sending_text4

    
def crawling_ksp():
    klayURL = 'https://coinmarketcap.com/ko/currencies/klaytn/'
    kspURL = 'https://coinmarketcap.com/ko/currencies/klayswap-protocol/'

    klay_result = requests.get(klayURL)
    ksp_result = requests.get(kspURL)

    klay_soup = BeautifulSoup(klay_result.text, "html.parser")
    ksp_soup = BeautifulSoup(ksp_result.text, "html.parser")

    klay_price = klay_soup.find("div", {"class": 'priceValue___11gHJ'}).text
    klay_price = klay_price[1:]
    klay_price = klay_price.replace(",", "")
    klay_price = float(klay_price)
    
    ksp_price = ksp_soup.find("div", {"class": 'priceValue___11gHJ'}).text
    ksp_price = ksp_price[1:]
    ksp_price = ksp_price.replace(",", "")
    ksp_price = float(ksp_price)
    
    ksp_value_rate = klay_price / ksp_price #현재
    ksp_swap_rate = 0.1311 #리밸런싱 시점-----------------------------------------------------------------------------------------------------------

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


    test = -1

    sending_text = "ksp 스왑비(예치시점): " + str(ksp_swap_rate) + "ksp\n"
    sending_text2 = "ksp 스왑비(현재): " + str(ksp_value_rate) + "ksp\n"
    sending_text3 = "ksp 스왑비 변동률: " + str(ksp_fluc) + "%" + memo + "\n"

    return sending_text + sending_text2 + sending_text3

def crawling_klay_shorts():
    klayURL = 'https://coinmarketcap.com/ko/currencies/klaytn/'
    daiURL = 'https://coinmarketcap.com/ko/currencies/multi-collateral-dai/'

    klay_result = requests.get(klayURL)
    dai_result = requests.get(daiURL)

    klay_soup = BeautifulSoup(klay_result.text, "html.parser")
    dai_soup = BeautifulSoup(dai_result.text, "html.parser")

    def crawling_price(k):
        price = k.find("div", {"class": 'priceValue___11gHJ'}).text
        price = price[1:]
        price = price.replace(",", "")
        price = float(price)
        return price

    klay_price = crawling_price(klay_soup)
    dai_price = crawling_price(dai_soup)

    klay_dai_rate = klay_price / dai_price
    klay_dai_rate = round(klay_dai_rate, 6)
    klay_dai_past = 2.872083 #리밸런싱 시점 ----------------------------------------------------------------------------------------------------
    
    klay_dai_fluc = klay_dai_rate - klay_dai_past
    klay_dai_fluc = klay_dai_fluc / klay_dai_past
    klay_dai_fluc = round(klay_dai_fluc * 100, 2)

    if klay_dai_fluc < 0:
        memo = "(klay 개수 증가중)"
    elif klay_dai_fluc == 0:
        memo = "(변동 없음)"
    else :
        memo = "(klay 개수 하락중 - 유동성제거 대기)"
    

    sending_text = "klay-dai 스왑비: " + str(klay_dai_rate) + "dai\n"
    sending_text2 = "klay-dai 변동률: " + str(klay_dai_fluc) + "%" + memo + "\n"

    return sending_text + sending_text2 , klay_dai_fluc


bot = telegram.Bot(token=my_token)

def sending_on_schedule():     #bot에 메세지 보내는 함수
    sending_text = crawling_ksp()
    sending_text2 = "----------------------------------\n"
    sending_text3, fluc = crawling_klay_shorts()
    text_sum = sending_text3 + sending_text2 + sending_text
    bot.sendMessage(chat_id=chat_id, text=text_sum)
    return fluc

gap = 0

def fluc_frequency():    #변동률 파일에 읽고쓰기 
    fluc = sending_on_schedule()
    def add():
        f = open("fluc.txt", 'a')
        data = str(fluc) 
        f.write(data)
        f.close()
    
    def read():
        f = open("fluc.txt", 'r')
        lines = f.readlines()
        index = []
        for line in lines:
            index.append(line)
        f.close()
        front = float(index[0])
        current = float(index[1])
        gap = current - front
        gap = abs(round(gap, 2))
        return gap
        
    def write():
        f = open("fluc.txt", 'w')
        data = str(fluc) + "\n"
        f.write(data)
        f.close()

    global gap
    add()
    gap = read()
    write()    

def whole_schedule():
    if gap > 2:
        puppet_ten_sec()
    elif gap > 1:
        puppet_one_min()
    elif gap > 0.5:
        puppet_five_min()
    else:
        pass

def main_schedule():    
    fluc_frequency()
    whole_schedule()

def ass_schedule():
    fluc_frequency()

def puppet_ten_sec():
    scheduler2 = schedule.Scheduler()
    scheduler2.every(10).seconds.do(ass_schedule)
    while True:
        scheduler2.run_pending()
        time.sleep(1)
        if gap <= 2:
            whole_schedule()
            break

def puppet_one_min():
    scheduler2 = schedule.Scheduler()
    scheduler2.every(1).minutes.do(ass_schedule)
    while True:
        scheduler2.run_pending()
        time.sleep(1)
        if gap <= 1:
            whole_schedule()
            break

def puppet_five_min():
    scheduler2 = schedule.Scheduler()
    scheduler2.every(5).minutes.do(ass_schedule)
    while True:
        scheduler2.run_pending()
        time.sleep(1)
        if gap <= 0.5:
            whole_schedule()
            break

main_schedule()
scheduler1 = schedule.Scheduler()
scheduler1.every(10).minutes.do(main_schedule)

while True:
    scheduler1.run_pending()
    time.sleep(1)
    
# sending_on_schedule()
# klay숏 하기 전 체크사항
# 스왑과 동시에 sending_on_schedule()실행 후 리밸런싱 시점 입력
# fluc.txt에 0입력



# print('start telegram chat bot')

# # message reply function
# def get_message(update, context) :
#     update.message.reply_text("got text")
#     update.message.reply_text(update.message.text)


# # rate reply function
# def keth_rate_command(update, context) :
#     keth = crawling_keth()
#     update.message.reply_text(keth)

# def ksp_rate_command(update, context) : 
#     ksp = crawling_ksp()
#     update.message.reply_text(ksp)


# updater = Updater(my_token, use_context=True)

# message_handler = MessageHandler(Filters.text & (~Filters.command), get_message) # 메세지중에서 command 제외
# updater.dispatcher.add_handler(message_handler)

# keth_rate_handler = CommandHandler('keth', keth_rate_command)
# updater.dispatcher.add_handler(keth_rate_handler)

# ksp_rate_handler = CommandHandler('ksp', ksp_rate_command)
# updater.dispatcher.add_handler(ksp_rate_handler)

# updater.start_polling(timeout=3, clean=True)
# updater.idle()