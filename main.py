# -*- coding: utf-8 -*-
import send
import os
from  quark import *
from jd_dou import *
import random
import time


    
def do():
    token = os.getenv('TOKEN')
    chat_id = os.getenv('CHAT_ID')
    quark_ck = os.getenv('QUARK_COOKIE')
    jd_ck = os.getenv('JD_COOKIE')
    delay = int(os.getenv('DELAY'))
    sender = send.Send(token)
    
    # 随机延期执行 30分钟-120分钟
    delay_time = random.randint(1800*delay, 7200*delay)
    print(f"{round(delay_time/60, 1)}分钟后开始执行")
    time.sleep(delay_time)
    if quark_ck:
        cookie_quark = [quark_ck]
        msg = ""
        print("✅检测到共", len(cookie_quark), "个夸克账号\n")

        i = 0
        while i < len(cookie_quark):
            # 开始任务
            log = f"🙍🏻‍♂️ 第{i + 1}个夸克账号"
            msg += log
            # 登录
            log = Quark(cookie_quark[i]).do_sign()
            msg += log + "\n"

            i += 1
        print(msg)
        sender.tg_send(chat_id, msg)
    # 随机延期执行 30分钟-120分钟
    delay_time = random.randint(1800*delay, 7200*delay)
    print(f"{round(delay_time/60, 1)}分钟后开始执行")
    time.sleep(delay_time)
    if jd_ck:
        cookie_jd = [jd_ck]
        msg = ""
        print("✅检测到共", len(cookie_quark), "个京东账号\n")
        
        i = 0
        while i < len(cookie_jd):
            # 开始任务
            log = f"🙍🏻‍♂️ 第{i + 1}个京东账号"
            msg += log
            # 登录
            log = signBeanAct(cookie_jd[i])
            msg += log + "\n"

            i += 1
        print(msg)
        sender.tg_send(chat_id, msg)
        
        

if __name__ == "__main__":
    do()
