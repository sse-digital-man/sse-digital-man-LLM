import codecs
import os
import sys
import random
import time
from datetime import datetime

from core import websocket_server
from core.scheduler.thread_manager import MyThread
# from utils import config_util

LOGS_PATH = "data/logs"
LOGS_FILE_URL = LOGS_PATH + '/' + "log-" + time.strftime("%Y%m%d%H%M%S") + ".log"

def cal_time(begin: datetime, end: datetime):
    sub_time = end - begin
    return sub_time.seconds + sub_time.microseconds / 1000000

def random_hex(length):
    result = hex(random.randint(0, 16 ** length)).replace('0x', '').lower()
    if len(result) < length:
        result = '0' * (length - len(result)) + result
    return result

def __write_to_file(text):
    if not os.path.exists(LOGS_PATH):
        os.mkdir(LOGS_PATH)
    file = codecs.open(LOGS_FILE_URL, 'a', 'utf-8')
    file.write(text + "\n")
    file.close()

def printInfo(level, sender, text, send_time=-1):
    if send_time < 0:
        send_time = time.time()
    format_time = time.strftime('%H:%M:%S', time.localtime(send_time))
    logStr = '[{}][{}] {}'.format(format_time, sender, text)
    print(logStr)
    if level >= 3:
        websocket_server.get_web_instance().add_cmd({"panelMsg": text})
        # if not config_util.config["interact"]["playSound"]: # 非展板播放
        #     content = {'Topic': 'Unreal', 'Data': {'Key': 'log', 'Value': text}}
        #     wsa_server.get_instance().add_cmd(content)
    # MyThread(target=__write_to_file, args=[logStr]).start()


# 清楚log缓存
def clear_log():
    if not os.path.exists(LOGS_PATH):
        os.mkdir(LOGS_PATH)
    for file_name in os.listdir(LOGS_PATH):
        if file_name.endswith('.log'):
            os.remove(LOGS_PATH + '/' + file_name)

def log(level, text):
    printInfo(level, "系统", text)

class DisablePrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout