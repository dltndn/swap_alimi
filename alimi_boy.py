import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules
import requests
from bs4 import BeautifulSoup

# bot = telegram.Bot(token='1601767622:AAGbhKM1WIccX0sOcfEpIazv7Mw1MBCabOU')

# bot.sendMessage(chat_id=chat_id, text=sending_text + "dkdl")

chat_id = 1343819766

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

    
upbit = 'https://upbit.com/home'
upbit_trends = 'https://upbit.com/trends'

my_token = '1601767622:AAGbhKM1WIccX0sOcfEpIazv7Mw1MBCabOU'

print('start telegram chat bot')

# message reply function
def get_message(update, context) :
    update.message.reply_text("got text")
    update.message.reply_text(update.message.text)


# rate reply function
def keth_rate_command(update, context) :
    keth = crawling_keth()
    update.message.reply_text(keth)


updater = Updater(my_token, use_context=True)

message_handler = MessageHandler(Filters.text & (~Filters.command), get_message) # 메세지중에서 command 제외
updater.dispatcher.add_handler(message_handler)

rate_handler = CommandHandler('get', keth_rate_command)
updater.dispatcher.add_handler(rate_handler)

updater.start_polling(timeout=3, clean=True)
updater.idle()