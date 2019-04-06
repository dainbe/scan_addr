#coding:utf-8
import time
import json
import datetime
import os
import requests

from get_addr import get_addr

sleep_time = 10
leave_min = 8
get_min = 1

get_time = datetime.datetime.now()

addr_list = []
time_list = []

path = "/home/pi/scan_addr/log.json"

SLACK_URL = "https://hooks.slack.com/services/hoge"

SYS_URL = "http://hoge"

GET_URL = "http://hige"

get_list = requests.get(GET_URL).json()
true_list = [x['address'] for x in get_list]

print(true_list)

try:
    os.remove(path)
except:
    pass

while True:
    new_mac_addr = set(get_addr())

    if ((datetime.datetime.now() - get_time).total_seconds() / 60) > get_min:

        get_list = requests.get(GET_URL).json()
        true_list = [x['address'] for x in get_list]

        for i in (set(true_list) - set(addr_list)):
            print(i)
            post_dic = {}
            post_dic['status'] = 0
            post_dic['addr'] = i
            print("{}".format(post_dic))

            try:
                j += 1
                requests.post(SYS_URL, post_dic)
            except:
                if j >= 10:
                    content = "[WARNING]:warning: 10 or more post errors :fast_parrot:"

                    payload = {
                        "text": content
                    }

                    data = json.dumps(payload)

                    requests.post(SLACK_URL, data)
                    break
                pass

            with open(path, "a") as f:
                f.write("LEAVE : addr | {}, enter_time | {}, leave_time | {}\n".format(
                    i, "Nan", datetime.datetime.now()))

            print("addr | {}, enter | {}, leave | {}".format(
                i, "Nan", datetime.datetime.now()))

        get_time = datetime.datetime.now()

    for i in new_mac_addr:
        if (i in addr_list) == False:
            addr_list.append(i)
            time_list.append(datetime.datetime.now())

            post_dic = {}
            post_dic['status'] = 1
            post_dic['addr'] = i
            print("{}".format(post_dic))

            j = 0
            try:
                j += 1
                r = requests.post(SYS_URL, post_dic)
                print(r.status_code)
            except:
                if j >= 10:
                    content = ":fast_parrot: エラーはいてるみたいですよ。:fast_parrot:"

                    payload = {
                        "text": content
                    }

                    data = json.dumps(payload)

                    requests.post(SLACK_URL, data)
                    break
                pass

            with open(path, "a") as f:
                f.write("ENTER : addr | {}, enter_time | {}\n".format(
                    i, datetime.datetime.now()))

        else:
            time_list[addr_list.index(i)] = datetime.datetime.now()

        print("addr | {}, enter | {}".format(i, time_list[addr_list.index(i)]))

    # leave
    for i in addr_list:
        time_list_index = addr_list.index(i)
        leave_time = time_list[time_list_index]

        if ((datetime.datetime.now() - leave_time).total_seconds() / 60) > leave_min:
            post_dic = {}
            post_dic['status'] = 0
            post_dic['addr'] = i
            print("{}".format(post_dic))
            try:
                j += 1
                requests.post(SYS_URL, post_dic)
            except:
                if j >= 10:
                    content = "[WARNING]:warning: 10 or more post errors :fast_parrot:"

                    payload = {
                        "text": content
                    }

                    data = json.dumps(payload)

                    requests.post(SLACK_URL, data)
                    break
                pass

            with open(path, "a") as f:
                f.write("LEAVE : addr | {}, enter_time | {}, leave_time | {}\n".format(
                    i, time_list[addr_list.index(i)], datetime.datetime.now()))

            print("addr | {}, enter | {}, leave | {}".format(
                i, time_list[addr_list.index(i)], datetime.datetime.now()))

            addr_list.remove(i)
            time_list.pop(time_list_index)

    print("===========================================================================================")

    time.sleep(sleep_time)
