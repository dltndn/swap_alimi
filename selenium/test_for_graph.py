import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler 
import schedule
import matplotlib.pyplot as plt
import numpy as np
import pickle

my_token = '1234'
chat_id = 1234

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

    with open('/home/ubuntu/important_data/data_fluc.txt', 'wb') as f:
        pickle.dump(data_list, f)

    

def draw_graph() :
    with open('/home/ubuntu/important_data/data_fluc.txt', 'rb') as f:
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

    plt.xlabel('date', fontsize=17)
    plt.ylabel('fluc', fontsize=17)

    plt.xticks(plot_x, label_list, fontsize=15)
    plt.yticks(np.arange(-100, 110, 10), ytick_list, fontsize=15)

    plt.legend(loc='best', fontsize=15)

    plt.tick_params(axis='x', direction='in', length=3, pad=6, top=True)

    plt.savefig('/home/ubuntu/important_data/save_graph.png', facecolor='#eeeeee', dpi = 200)

# print('start telegram chat bot')

bot = telegram.Bot(token=my_token)
# message reply function
def get_message(update, context) :
    update.message.reply_text("got text")
    update.message.reply_text(update.message.text)


# rate reply function
def get_graph_image(update, context) :
    bot.sendPhoto(chat_id=chat_id, photo=open('/home/ubuntu/important_data/save_graph.png', 'rb'))

updater = Updater(my_token, use_context=True)

message_handler = MessageHandler(Filters.text & (~Filters.command), get_message) # 메세지중에서 command 제외
updater.dispatcher.add_handler(message_handler)

keth_rate_handler = CommandHandler('graph', get_graph_image)
updater.dispatcher.add_handler(keth_rate_handler)

updater.start_polling(timeout=3, clean=True)
updater.idle()

