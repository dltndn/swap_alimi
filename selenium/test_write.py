import telegram
import pickle

my_token = '1234'
chat_id = 1234

data = "hello world"
        

with open('/home/ubuntu/important_data/data_test.txt', 'wb') as f:
    pickle.dump(data, f)

with open('/home/ubuntu/important_data/data_test.txt', 'rb') as f:
    data = pickle.load(f)
    text_sum = data

bot = telegram.Bot(token=my_token)
bot.sendMessage(chat_id=chat_id, text=text_sum)
    


