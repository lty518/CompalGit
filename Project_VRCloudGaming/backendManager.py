# ConnectionManager
import requests
import socket
import sys
import os
import logging
import psutil
import time
from requests import get, post, exceptions
from multiprocessing import Process
import check_vm_information as vm
local_ip = ''
# logging.basicConfig(level=logging.DEBUG)
# Register to manager


def RegisterToBackendServer(backend_ip, installedGameList):
    global local_ip
    local_ip = socket.gethostbyname(socket.gethostname())
    # sys.set('LOCAL_IP',local_ip)
    data = {'edge_ip': local_ip, 'games': installedGameList}
    try:
        r = post('http://{0}//register'.format(backend_ip), data=data)
        logging.info("register_to_backend_server" + r.text)
        print("register_to_backend_server" + r.text)
    except exceptions.RequestException as e:
        raise SystemExit(e)


def UnregisterToBackendServer(backend_ip):
    print("UnregisterToBackednServer : ", backend_ip)
    res = get('http://{0}//deregister'.format(backend_ip))
    print(res.text)


def SendGameTimeout(BACKEND_SERVER_IP):
    data = {'connection_status': 'timeout'}

    server_ip = BACKEND_SERVER_IP
    url = 'http://' + server_ip + '/connection-status'
    r = requests.post(url, data=data)
    # r = requests.post('http://172.16.0.189:5000/connection-status', data=data)
    # r = requests.get('http://127.0.0.1:8080/', params = my_data)
    # And done.
    print('r.url :', r.url)
    print('r.text : ', r.text)  # displays the result body.


def SendGameConnection(BACKEND_SERVER_IP, client_ip, game_id, connection_status):
    data = {'client_ip': client_ip, 'game_id': game_id,
            'connection_status': connection_status}

    server_ip = BACKEND_SERVER_IP
    url = 'http://' + server_ip + '/connection-status'
    r = requests.post(url, data=data)
    # r = requests.post('http://172.16.0.189:5000/connection-status', data=data)
    # r = requests.get('http://127.0.0.1:8080/', params = my_data)
    # And done.
    print('r.url :', r.url)
    print('r.text : ', r.text)  # displays the result body.

def SendSystemHeartbeat(BACKEND_SERVER_IP):
    # p = psutil.Process(input_pid)
    # print(p.name())  #程序名
    # print(p.exe())  #程序的bin路徑
    # print(p.cwd())  #程序的工作目錄絕對路徑
    # print(p.status())  #程序狀態
    # print(p.create_time()) #程序建立時間
    # # print(p.uids())  #程序uid資訊
    # # print(p.gids())  #程序的gid資訊
    # print(p.cpu_times())  #程序的cpu時間資訊,包括user,system兩個cpu資訊
    # print(p.cpu_affinity()) #get程序cpu親和度,如果要設定cpu親和度,將cpu號作為參考就好
    # print(p.memory_percent()) #程序記憶體利用率
    # print(p.memory_info())  #程序記憶體rss,vms資訊
    # print(p.io_counters())  #程序的IO資訊,包括讀寫IO數字及引數
    # # print(p.connectios())  #返回程序列表
    # print(p.num_threads()) #程序開啟的執行緒數
    # data = {'name': p.name(),
    #         'exe': p.exe(),
    #         'cwd': p.cwd(),
    #         'status': p.status(),
    #         'create_time': p.create_time(),
    #         'cpu_times': p.cpu_times(),
    #         'cpu_affinity': p.cpu_affinity(),
    #         'memory_percent': p.memory_percent(),
    #         'memory_info': p.memory_info(),
    #         'io_counters': p.io_counters(),
    #         'num_threads': p.num_threads()
    #         }
    global local_ip
    while True:
        data = {'cpu': vm.cpu(),
                'memory': vm.memory(),
                'disk': vm.disk(),
                'GPU' : vm.parse_nvidia_smi()['Gpu'],
                'ip' : local_ip,
                'status': 'TODO',
                'current_game': 'TODO',
                'network_io': 'TODO'
                }
        url = 'http://' + BACKEND_SERVER_IP + '/heartbeat'
        requests.post(url, data=data)
        time.sleep(30)

def test_connect():
        data = {'test': 'test'}
        url = 'http://' + '172.16.0.189:5000' + '/heartbeat'
        requests.post(url, data=data)
""" Uncomment below to debug"""
# SendGameConnection("172.16.0.189","123","456","0")
# if __name__ == '__main__':
#     dict = {'BACKEND_SERVER_IP' : '172.16.0.189:5000', 'client_ip': 'client_ip',
#     'game_id': 'game_id', 'game_title' : 'game_title'}
#     p = Process(target = SendSystemHeartbeat, args=(dict,))
#     p.start()