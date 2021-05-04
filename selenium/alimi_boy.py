import telegram
#from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules
import requests
from bs4 import BeautifulSoup
import schedule
import time
import pickle

my_token = '1234'
chat_id = 1234


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
    kspURL = 'https://www.coingecko.com/ko/%EC%BD%94%EC%9D%B8/klayswap-protocol'
    dollar_rate_URL = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%ED%99%98%EC%9C%A8' 

    klay_result = requests.get(klayURL)
    ksp_result = requests.get(kspURL)
    dollar_result = requests.get(dollar_rate_URL)

    klay_soup = BeautifulSoup(klay_result.text, "html.parser")
    ksp_soup = BeautifulSoup(ksp_result.text, "html.parser")
    dollar_soup = BeautifulSoup(dollar_result.text, "html.parser")

    klay_price = klay_soup.find("div", {"class": 'priceValue___11gHJ'}).text
    klay_price = klay_price[1:]
    klay_price = klay_price.replace(",", "")
    klay_price = float(klay_price)
    
    ksp_price = ksp_soup.find("span", {"class": 'no-wrap'}).text
    ksp_price = ksp_price[1:]
    ksp_price = float(ksp_price)

    dollar_rate = dollar_soup.find("span", {"class": "spt_con"}).find("strong").text
    dollar_rate = dollar_rate[:5]
    dollar_rate = dollar_rate.replace(",", "")
    dollar_rate = float(dollar_rate)
    
    ksp_price_krw = ksp_price * dollar_rate
    
    ksp_value_rate = klay_price / ksp_price_krw #현재
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

def crawling_orc():
    klayURL = 'https://coinmarketcap.com/ko/currencies/klaytn/'
    orcURL = 'https://coinmarketcap.com/ko/currencies/orbit-chain/'

    klay_result = requests.get(klayURL)
    orc_result = requests.get(orcURL)

    klay_soup = BeautifulSoup(klay_result.text, "html.parser")
    orc_soup = BeautifulSoup(orc_result.text, "html.parser")

    klay_price = klay_soup.find("div", {"class": 'priceValue___11gHJ'}).text
    klay_price = klay_price[1:]
    klay_price = klay_price.replace(",", "")
    klay_price = float(klay_price)
    
    orc_price = orc_soup.find("div", {"class": 'priceValue___11gHJ'}).text
    orc_price = orc_price[1:]
    orc_price = orc_price.replace(",", "")
    orc_price = float(orc_price)
    
    orc_value_rate = klay_price / orc_price #현재
    orc_swap_rate = 0.956 #리밸런싱 시점-----------------------------------------------------------------------------------------------------------

    orc_fluc = orc_value_rate - orc_swap_rate
    orc_fluc = orc_fluc / orc_swap_rate
    orc_fluc = round(orc_fluc * 100, 2)

    orc_value_rate = round(orc_value_rate, 4)
    orc_swap_rate = round(orc_swap_rate, 4)

    if orc_fluc < 0:
        memo = "(klay 가치- 개수+)"
    elif orc_fluc == 0:
        memo = "(변동 없음)"
    else :
        memo = "(klay 가치+ 개수-)"

    sending_text = "klay-orc 스왑비(예치시점): " + str(orc_swap_rate) + "orc\n"
    sending_text2 = "klay-orc 스왑비(현재): " + str(orc_value_rate) + "orc\n"
    sending_text3 = "klay-orc 스왑비 변동률: " + str(orc_fluc) + "%" + memo + "\n"

    orc_fluc = float(orc_fluc)

    return sending_text + sending_text2 + sending_text3, orc_fluc

def crawling_ksp_orc():
    kspURL = 'https://www.coingecko.com/ko/%EC%BD%94%EC%9D%B8/klayswap-protocol'
    orcURL = 'https://coinmarketcap.com/ko/currencies/orbit-chain/'
    dollar_rate_URL = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%ED%99%98%EC%9C%A8'

    ksp_result = requests.get(kspURL)
    orc_result = requests.get(orcURL)
    dollar_result = requests.get(dollar_rate_URL)

    ksp_soup = BeautifulSoup(ksp_result.text, "html.parser")
    orc_soup = BeautifulSoup(orc_result.text, "html.parser")
    dollar_soup = BeautifulSoup(dollar_result.text, "html.parser")
    
    orc_price = orc_soup.find("div", {"class": 'priceValue___11gHJ'}).text
    orc_price = orc_price[1:]
    orc_price = orc_price.replace(",", "")
    orc_price = float(orc_price)

    ksp_price = ksp_soup.find("span", {"class": 'no-wrap'}).text
    ksp_price = ksp_price[1:]
    ksp_price = float(ksp_price)

    dollar_rate = dollar_soup.find("span", {"class": "spt_con"}).find("strong").text
    dollar_rate = dollar_rate[:5]
    dollar_rate = dollar_rate.replace(",", "")
    dollar_rate = float(dollar_rate)
    
    ksp_price_krw = ksp_price * dollar_rate
    
    orc_value_rate = ksp_price_krw / orc_price #현재
    orc_swap_rate = 18.909 #리밸런싱 시점-----------------------------------------------------------------------------------------------------------

    orc_fluc = orc_value_rate - orc_swap_rate
    orc_fluc = orc_fluc / orc_swap_rate
    orc_fluc = round(orc_fluc * 100, 2)

    orc_value_rate = round(orc_value_rate, 4)
    orc_swap_rate = round(orc_swap_rate, 4)

    if orc_fluc < 0:
        memo = "(ksp 가치- 개수+)"
    elif orc_fluc == 0:
        memo = "(변동 없음)"
    else :
        memo = "(ksp 가치+ 개수-)"

    sending_text = "ksp-orc 스왑비(예치시점): " + str(orc_swap_rate) + "orc\n"
    sending_text2 = "ksp-orc 스왑비(현재): " + str(orc_value_rate) + "orc\n"
    sending_text3 = "ksp-orc 스왑비 변동률: " + str(orc_fluc) + "%" + memo + "\n"

    orc_fluc = float(orc_fluc)

    return sending_text + sending_text2 + sending_text3, orc_fluc

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
    klay_dai_past = 4.119186 #리밸런싱 시점 ----------------------------------------------------------------------------------------------------
    
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

bot = telegram.Bot(token=my_token)

def sending_on_schedule():     #bot에 메세지 보내는 함수
    dotted_line = "------------------------------\n"
    sending_text3, ksp_orc = crawling_ksp_orc()
    sending_text, klay_orc = crawling_orc()
    sending_text4, bnb_belt = crawling_bnb_belt()
    # sending_text5 = crawling_ksp()
    text_sum = sending_text3 + dotted_line + sending_text + dotted_line + sending_text4 #+ dotted_line + sending_text5
    bot.sendMessage(chat_id=chat_id, text=text_sum)
    # return fluc

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

sending_on_schedule()
scheduler1 = schedule.Scheduler()
scheduler1.every(15).minutes.do(sending_on_schedule)

while True:
    scheduler1.run_pending()
    time.sleep(1)



