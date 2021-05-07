# flask_simple_server
import atexit
import glob
import logging
import os
import subprocess
import socket
import sys
import threading
import time
import json
import requests
from multiprocessing import Process
from os import path
from threading import Timer

from flask import Flask, request
from requests import exceptions, get, post

import backendManager as bm
import check_if_port_open
import obs_websocket as obs
import steamVRManager as svrm
import systemSettings as sys
import udp_client_listener as ucl
# -----------------------------
import checkInstalledGame as ch

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
# app_id
TEAMVR_GAMEID = '250820'
HELLBLADE = '747350'
STEAMVR_ID = '250820'
# GAME_NAME
SteamVR = 'vrserver'


# IP
CLOUDXR_SERVER_MANAGER_IP = ''
CLOUDXR_CLIENT_IP = ''
BACKEND_SERVER_IP = ''
# FLAG
is_available = True
app_id = ''
app_title = ''
player_ip = ''
platform = ''
applist = list()
# GlOBAL VARIABLES
launch_time = time.time()
g_CurrentGameID = ''
settings = ''

@app.route('/connection-timeout', methods=['GET'])
def timeoutCloudXR():
    svrm.timeoutOpenGame(BACKEND_SERVER_IP)
    global is_available
    is_available = True
    print("timeoutCloudXR")

# check if steamvr is ok and return ready for a user to connect
@app.route('/game-connection', methods=['POST', 'GET'])
def launchCloudXR():
    if request.method == 'POST':
        print('============launchCloudXR=============')
        global player_ip, is_available, app_title, platform
        global app_id
        global BACKEND_SERVER_IP
        # if not is_available:
        #     return 'Game server not available now'
        app_title = request.form.get('app_title', type=str)
        app_id = request.form.get('app_id', type=str)
        player_ip = request.form.get('player_ip', type=str)
        platform = request.form.get('platform', type = str)
        print('platform: ', platform)

        svrm.setAppID(app_id)
        svrm.setAppTitle(app_title)
        svrm.setAppPlatform(platform)

        # logging.info("request: {0} {1} {2}".format(app_title,  app_id, player_ip))

        if svrm.CheckGameStatus(SteamVR) >= 1:
            if platform == "steam" or platform == "compal":
                if is_available == True:
                    svrm.startGame(BACKEND_SERVER_IP, player_ip,
                                app_id, app_title, platform)
                is_available = False
                return {'launch success': True}
            else:
                return {'launch success': False}
        else:
            svrm.startSteamvr(STEAMVR_ID)
            while svrm.CheckGameStatus(SteamVR) == 0:
                continue
            # TODO: open steamvr again and startGame
            # TODO: return false if error happen
            return {'launch success': False}
    # for launching steamVR process
    else:
        #should return exception when packet is not POST
        if time.time() > launch_time+10:
            return {'status': True}
        else:
            return {'status': False}

@app.route('/game-disconnection', methods=['POST'])
def closeCloudXR():
    global player_ip, is_available, app_id, app_title,platform
    # print(player_ip, request.remote_addr)
    # app_title = request.form.get('app_title', type=str)
    # app_id = request.form.get('app_id', type=str)
    # if request.remote_addr != player_ip and player_ip != '127.0.0.1':
    #     return 'Invalid request'

    # Close game app and steamVR, and reset game server status
    print('closeCloudXR : ', svrm.getAppTitle())
    logging.info(svrm.getAppTitle())
    # if g_CurrentGameTitle == '':
    #     return {'close fail': False, 'app_title' : app_title}
    if svrm.CheckGameStatus(svrm.getAppTitle()) >= 1:
        #close the current game
        cur_platform = svrm.getAppPlatform()
        # print('cur_platform: ', cur_platform)
        if cur_platform == 'steam':
            svrm.closeGame(svrm.getAppTitle())
        elif cur_platform =='compal':
            print('svrm.getApplication: ', svrm.getApplication())
            svrm.closeApplication(svrm.getAppTitle(), svrm.getApplication())
        #close the steamvr
        time.sleep(5)
        svrm.closeSteamvr()
        #close obs streaming
        stream_server_ip = settings['STREAM_SERVER_IP']
        obs.stop(BACKEND_SERVER_IP,stream_server_ip)
        #set game server to be available again
        is_available = True
        #print(player_ip, is_available)
        time.sleep(5)
        #restart steamvr
        svrm.startSteamvr(STEAMVR_ID)
        while svrm.CheckGameStatus(SteamVR) == 0:
            continue
        #send status to backend server
        bm.SendGameConnection(BACKEND_SERVER_IP, player_ip, app_id, "closed",platform)
        svrm.setAppID('')
        player_ip = ''

        # RegisterToBackednServer()
        return {'close success': True, 'app_title': app_title}
    elif svrm.CheckGameStatus(SteamVR) >= 1:
        svrm.closeSteamvr()
        bm.SendGameConnection(BACKEND_SERVER_IP, player_ip, app_id, "closed",platform)
        svrm.setAppID('')
        player_ip = ''
        #add delay
        time.sleep(5)
        #restart steamvr
        svrm.startSteamvr(STEAMVR_ID)
        while svrm.CheckGameStatus(SteamVR) == 0:
            continue
        return {'close success': True, 'app_title': app_title}
    else:
        return {'close success': False, 'app_title': app_title}

@app.route('/steamvr-status', methods=['POST', 'GET'])
def getSteamVRStatus():
    if svrm.CheckGameStatus(SteamVR) >= 1:
        return {'SteamVR Status': True}
    else:
        return {'SteamVR Status': False}


@app.route('/game-status', methods=['POST', 'GET'])
def getGameStatus():
    # app_id = request.form.get('app_id', type=str)
    app_title = request.form.get('app_title', type=str)
    if svrm.CheckGameStatus(app_title) >= 1:
        return {'app_id Status': True, 'app_title': app_title}
    else:
        return {'app_id Status': False, 'app_title': app_title}

@app.route('/reconnect_to_backend_server', methods=['POST', 'GET'])
def reconnect_to_backend_server():
    bm.RegisterToBackendServer(BACKEND_SERVER_IP, applist)
    return {'app_id Status': True}

@app.route('/start_droid_cam', methods=['POST', 'GET'])
def start_droid_cam():
    app_title = request.form.get('app_title', type=str)
    app_type = request.form.get('app_type', type = str)
    print('start_droid_cam app_title: ', app_title)
    print('start_droid_cam app_type: ', app_type)
    with open(os.path.relpath('GamingServer/appdict.json')) as f:
        data = json.load(f)
    for json_dict in data:
        if json_dict['App'] == app_title:
            svrm.setApplication(json_dict['Application'])
            #request the ip
            my_params = {
                    'protocol': app_type,
                    'app_name': app_title
                    }
            url = 'http://' + BACKEND_SERVER_IP + '/dataflow'
            r = requests.get(url, params=my_params)
            print("status_code: ", r.status_code)
            json_data = json.loads(r.text)
            # start camera
            if json_data['status'] == True:
                path = json_dict['DroidCam_Path']
                subprocess.Popen([ path, '-c', json_data['source_url'], '4747', '-video'])
    return json_data

@app.route('/obs_start_streaming', methods=['POST', 'GET'])
def obs_start_streaming():
    global player_ip
    print("obs_start_streaming")
    stream_server_ip = settings['STREAM_SERVER_IP']
    obs.start(BACKEND_SERVER_IP,stream_server_ip ,player_ip)
    dict = {
        'status' : True,
        'msg': 'TODO'
    }
    return dict

@app.route('/obs_stop_streaming', methods=['POST', 'GET'])
def obs_stop_streaming():
    print("obs_stop_streaming")
    stream_server_ip = settings['STREAM_SERVER_IP']
    obs.stop(BACKEND_SERVER_IP,stream_server_ip)
    dict = {
        'status' : True,
        'msg': 'TODO'
    }
    return dict

def main():
    global BACKEND_SERVER_IP
    global applist
    global settings
    # check installed steamvr games in pc
    ch.CheckInstalledSteamGame(applist)
    ch.CheckInstalledNonSteamApplication(applist)
    print(applist)
    if len(applist) == 0:
        print('applist is empty')
    # ucl.start_udp_server()
    settings = sys.loadConfig()
    # if sys not true return error
    BACKEND_SERVER_IP = settings['BACKEND_SERVER_IP']
    # register to backed server
    bm.RegisterToBackendServer(BACKEND_SERVER_IP, applist)
    # if fail to RegisterToBackednServer

    # then throw exceptions

    # if steamVR not open
    if svrm.CheckGameStatus(SteamVR) == 0:
        print("SteamVR is not running, open now!")
        svrm.startSteamvr(STEAMVR_ID)
        while svrm.CheckGameStatus(SteamVR) == 0:
            continue
    else:
        print("SteamVR is running!")

    atexit.register(bm.UnregisterToBackendServer, BACKEND_SERVER_IP)
    # atexit.register(ucl.stop_udp_server)
    # create a while-while to listen to steamvr messages
    # CheckSteamVRLogs
    # if logs updated
    # send status to backed server
    # loop


if __name__ == '__main__': 
    # set host='0.0.0.0', port=80 to enable external access in local network
    # app.debug = True
    # app.use_reloader=False
    main()
    # check_if_port_open.check(
    #     settings['GAMESERVER_IP'], settings['GAMESERVER_PORT'])

    # send Heartbeat to backend
    if False:
        dict = {'BACKEND_SERVER_IP': settings['GAMESERVER_IP'], 'client_ip': 'client_ip',
                'app_id': 'app_id', 'app_title': 'app_title'}
        p = Process(target=bm.SendSystemHeartbeat, args=(dict,))
        p.start()

    # add thread to send heartbeat to backend
    app.run(host=settings['GAMESERVER_IP'], port=settings['GAMESERVER_PORT'])
