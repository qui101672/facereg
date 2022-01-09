from pymongo import MongoClient
import server_config
from datetime import date
import time


def db_connect(col_name):
    client = MongoClient(server_config.MONGO_CONFIG)
    db = client["userDb"]
    cols = db[col_name]
    return cols


# names = ["Kha Thiên Duy", "Lê Hoàng Quí","Lê Trung Hưng", "Lương Chín Nguyên", "Nguyễn Vân Đoan", "Nguyễn Văn Võ","Phạm Trung Nghĩa", "Trần Thanh Thanh","Vũ Ngọc Huệ Trân","Lee Do-Hyun", "Park Shin Hye", "Hirai Momo"]
# stt=0
# for name in names:
#     cols = db_connect("users")
#     today = date.today()
#     current_date = today.strftime("%d/%m/%Y")
#     user = {'_id': stt, 'full_name': name, 'created_date': current_date, 'log_id': stt, 'last_checked': ""}
#     cols.insert_one(user)
#     stt += 1

# cols = db_connect("users")
# today = date.today()
# current_date = today.strftime("%d/%m/%Y")
# user = {'_id': 12, 'full_name': "Đào Chí Bửu", 'created_date': current_date, 'log_id': 12, 'last_checked': ""}
# cols.insert_one(user)



def get_max_id():
    list_id = list()
    cols = db_connect("users")
    results = cols.find({})
    for id in results:
        list_id.append(id['_id'])
    max_id = max(list_id)
    return max_id


def get_current_datetime():
    today = date.today()
    current_date = today.strftime("%d/%m/%Y")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time, current_date

def insert_user(name):
    cols = db_connect("users")
    current_date = get_current_datetime()
    stt = get_max_id() + 1
    user = {'_id': stt, 'full_name': name, 'created_date': current_date[1], 'last_checked': ""}
    cols.insert_one(user)


def insert_checkin_log(id):
    cols = db_connect("checkin_logs")
    current_time, current_date = get_current_datetime()
    log = {'user_id': id, 'check_time': current_time, 'check_date': current_date}
    current_datetime = current_date + " " + current_time
    cols.insert_one(log)
    update_last_checked(id, current_datetime)


def update_last_checked(id, last_checked):
    cols = db_connect("users")
    cols.update_one({'_id': id}, {"$set": {'last_checked': last_checked}})



def find_user_name(id):
    cols = db_connect("users")
    name = cols.find_one({'_id': id})
    return name["full_name"]

def get_users():
    users = list()
    cols = db_connect("users")
    records = cols.find({}, {'_id':0})
    for record in records:
        users.append(record)
    return users




