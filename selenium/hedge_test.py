import requests
from bs4 import BeautifulSoup

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
    klay_dai_past = 3.085865 #리밸런싱 시점
    
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
    sending_text2 = "klay-dai 변동률: " + str(klay_dai_fluc) + "%\n"

    return sending_text + sending_text2

print(crawling_klay_shorts())

