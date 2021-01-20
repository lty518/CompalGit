# ConnectionManager
import requests
import socket
import sys
import os
import logging
from requests import get, post, exceptions
local_ip =''
# logging.basicConfig(level=logging.DEBUG)
# Register to manager
def RegisterToBackednServer(backend_ip, installedGameList):
    global local_ip
    local_ip = socket.gethostbyname(socket.gethostname())
    # sys.set('LOCAL_IP',local_ip)
    data = {'edge_ip': local_ip, 'games': installedGameList}
    try:
        r = post('http://{0}//register'.format(backend_ip), data= data)
        logging.info("register_to_backend_server" + r.text)
        print ("register_to_backend_server" + r.text)
    except exceptions.RequestException as e:
        raise SystemExit(e)

def UnregisterToBackednServer(backend_ip):
    print("UnregisterToBackednServer : ", backend_ip)
    res = get('http://{0}//deregister'.format(backend_ip))
    print(res.text)

def SendGameConnection(BACKEND_SERVER_IP,client_ip, game_id, connection_status):
    data = {'client_ip': client_ip, 'game_id': game_id,
            'connection_status': connection_status}

    server_ip = BACKEND_SERVER_IP
    url = 'http://' + server_ip +'/connection-status'
    r = requests.post(url, data=data)
    # r = requests.post('http://172.16.0.189:5000/connection-status', data=data)
    # r = requests.get('http://127.0.0.1:8080/', params = my_data)
    # And done.
    print(r.url)
    print(r.text)  # displays the result body.

""" Uncomment below to debug"""
# SendGameConnection("172.16.0.189","123","456","0")
