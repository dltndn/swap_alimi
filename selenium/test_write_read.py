import pickle
import telegram

my_token = '1234'
chat_id = 1234

data = "hello world"
with open('data_fluc.txt', 'wb') as f:
    pickle.dump(data, f)


with open('data_fluc.txt', 'rb') as f:
        data = pickle.load(f)
        text_sum =data
        

bot = telegram.Bot(token=my_token)
bot.sendMessage(chat_id=chat_id, text=text_sum)

