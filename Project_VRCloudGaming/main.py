# flask_simple_server
import atexit
import glob
import logging
import os
from multiprocessing import Process
import socket
import sys
import threading
import time
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
from checkInstalledGame import CheckInstalledGame

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
# GAME_ID
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
game_id = ''
game_title = ''
player_ip = ''
list = ''
# GlOBAL VARIABLES
launch_time = time.time()
g_CurrentGameID = ''
settings = ''


@app.route('/')
def hello():
    return "<h1>Hello World!</h1>"


@app.route("/hello/<text>")
def index(text):
    print(text)
    return "<h1>%s</h1>" % text


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
        global player_ip, is_available, game_title
        global game_id
        global BACKEND_SERVER_IP
        # if not is_available:
        #     return 'Game server not available now'
        game_title = request.form.get('game_title', type=str)
        game_id = request.form.get('game_id', type=str)
        player_ip = request.form.get('player_ip', type=str)

        svrm.setGameID(game_id)
        svrm.setGameTitle(game_title)
        # logging.info("request: {0} {1} {2}".format(game_title,  game_id, player_ip))
        # Game_id needs to be generalized
        if svrm.CheckGameStatus(SteamVR) >= 1:
            if is_available == True:
                svrm.startGame(BACKEND_SERVER_IP, player_ip,
                               game_id, game_title)
            is_available = False
            # bm.SendGameConnection(BACKEND_SERVER_IP,player_ip, game_id, "playing")
            return {'launch success': True}
        else:
            # TODO: open steamvr again and startGame
            # TODO: return false if error happen
            return {'launch success': False}
    # for launching steamVR process
    else:
        if time.time() > launch_time+10:
            return {'status': True}
        else:
            return {'status': False}


@app.route('/game-disconnection', methods=['POST'])
def closeCloudXR():
    global player_ip, is_available, game_id, game_title
    # print(player_ip, request.remote_addr)
    # game_title = request.form.get('game_title', type=str)
    #game_id = request.form.get('game_id', type=str)
    # if request.remote_addr != player_ip and player_ip != '127.0.0.1':
    #     return 'Invalid request'
    # Close game app and steamVR, and reset game server status
    print('closeCloudXR : ', svrm.getGameTitle())
    logging.info(svrm.getGameTitle())
    # if g_CurrentGameTitle == '':
    #     return {'close fail': False, 'game_title' : game_title}
    if svrm.CheckGameStatus(svrm.getGameTitle()) >= 1:
        svrm.closeGame(svrm.getGameTitle())
        is_available = True
        print(player_ip, is_available)
        bm.SendGameConnection(BACKEND_SERVER_IP, player_ip, game_id, "closed")
        svrm.setGameID('')
        player_ip = ''
        # RegisterToBackednServer()
        return {'close success': True, 'game_title': game_title}
    else:
        return {'close success': False, 'game_title': game_title}


@app.route('/stream-info')
def getStreamInfo():
    return 'Under construction'


@app.route('/steamvr-status', methods=['POST', 'GET'])
def getSteamVRStatus():
    if svrm.CheckGameStatus(SteamVR) >= 1:
        return {'SteamVR Status': True}
    else:
        return {'SteamVR Status': False}


@app.route('/game-status', methods=['POST', 'GET'])
def getGameStatus():
    # game_id = request.form.get('game_id', type=str)
    game_title = request.form.get('game_title', type=str)
    if svrm.CheckGameStatus(game_title) >= 1:
        return {'game_id Status': True, 'game_title': game_title}
    else:
        return {'game_id Status': False, 'game_title': game_title}


@app.route('/reconnect_to_backend_server', methods=['POST', 'GET'])
def reconnect_to_backend_server():
    bm.RegisterToBackendServer(BACKEND_SERVER_IP, list)
    return {'game_id Status': True}


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
    global list
    global settings
    # check installed steamvr games in pc
    list = CheckInstalledGame()
    # if list is empty
    # return
    # ucl.start_udp_server()
    settings = sys.loadConfig()
    # if sys not true return error
    BACKEND_SERVER_IP = settings['BACKEND_SERVER_IP']
    # register to backed server
    bm.RegisterToBackendServer(BACKEND_SERVER_IP, list)
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
                'game_id': 'game_id', 'game_title': 'game_title'}
        p = Process(target=bm.SendSystemHeartbeat, args=(dict,))
        p.start()

    # add thread to send heartbeat to backend
    app.run(host=settings['GAMESERVER_IP'], port=settings['GAMESERVER_PORT'])
