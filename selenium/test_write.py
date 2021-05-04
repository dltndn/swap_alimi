import pickle

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


    with open('/home/ubuntu/important_data/data_fluc.txt', 'wb') as f:
        pickle.dump(data_list, f)
    

write_data()

