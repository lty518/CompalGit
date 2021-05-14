import threading
import time
import os
import subprocess
import psutil

def get_process_count(imagename):
    p = os.popen('tasklist /FI "IMAGENAME eq %s"' % imagename)
    return p.read().count(imagename)
def timer_start():
    t = threading.Timer(120,watch_func,("is running…"))
    t.start()
def watch_func(msg):
    if get_process_count('main.exe') == 0 :
        print(subprocess.Popen([r'D:\shuaji\bin\main.exe']))
    timer_start()

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

if __name__ == "__main__":
    if "vrserver.exe" in (p.name() for p in psutil.process_iter()):
        print("true")
    else:
        print("false")
    # if process_exists('SteamVR.exe'):
    #     print ("SteamVR is running!")
    # else:
    #     print("SteamVR is not running!")

    # timer_start()
    # while True:
    # time.sleep(1)
