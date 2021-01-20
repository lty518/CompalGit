#flask_simple_server
import sys
import os
import threading
import time
import subprocess
import glob
import atexit
from requests import get, post, exceptions
from flask import Flask, request
import time
from threading import Timer
import subprocess
import socket
from os import path
import logging
import openvr
#-----------------------------
from checkInstalledGame import CheckInstalledGame
import backendManager as bm
import systemSettings as sys
import steamVRManager as svrm
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
#GAME_ID
TEAMVR_GAMEID = '250820'
HELLBLADE = '747350'
STEAMVR_ID = '250820'
#GAME_NAME
SteamVR = 'vrserver'


#IP
CLOUDXR_SERVER_MANAGER_IP = ''
CLOUDXR_CLIENT_IP = ''
BACKEND_SERVER_IP = ''
#FLAG
is_available = 1
game_id =''
game_title = ''
player_ip = ''
list = ''
#GlOBAL VARIABLES
launch_time = time.time()
g_CurrentGameID = ''

@app.route('/')
def hello():
    return "<h1>Hello World!</h1>"

@app.route("/hello/<text>")
def index(text):
    print(text)
    return "<h1>%s</h1>" % text

#check if steamvr is ok and return ready for a user to connect
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
        print("======request: ", game_title, game_id, player_ip)
        # Game_id needs to be generalized
        if svrm.CheckGameStatus(SteamVR) >= 1:
            is_available = 0
            print('Available: ', is_available)
            svrm.startGame(BACKEND_SERVER_IP,player_ip, game_id, game_title)
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
        is_available = 1
        print(player_ip, is_available)
        bm.SendGameConnection(BACKEND_SERVER_IP,player_ip, game_id, "closed")
        svrm.setGameID('')
        player_ip = ''
        # RegisterToBackednServer()
        return {'close success': True, 'game_title' : game_title}
    else:
        return {'close success': False, 'game_title' : game_title}

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
    game_id = request.form.get('game_id', type=str)
    game_title = request.form.get('game_title', type=str)
    if svrm.CheckGameStatus(game_title) >= 1:
        return {'game_id Status': True, 'game_title' : game_title}
    else:
        return {'game_id Status': False, 'game_title' : game_title}

@app.route('/reconnect_to_backend_server', methods=['POST', 'GET'])
def reconnect_to_backend_server():
    bm.RegisterToBackednServer(BACKEND_SERVER_IP, list)
    return {'game_id Status': True}

def main():
    global BACKEND_SERVER_IP, list
    # check installed steamvr games in pc
    list = CheckInstalledGame()
    #if list is empty
    # return
    settings = sys.loadConfig()
    #if sys not true return error
    BACKEND_SERVER_IP = settings['BACKEND_SERVER_IP']
    # register to backed server
    bm.RegisterToBackednServer(BACKEND_SERVER_IP, list)
    #if steamVR not open
    if svrm.CheckGameStatus(SteamVR) == 0:
        print ("SteamVR is not running, open now!")
        svrm.startSteamvr(STEAMVR_ID)
        while svrm.CheckGameStatus(SteamVR) == 0 :
            continue
    else:
        print("SteamVR is running!")

    atexit.register(bm.UnregisterToBackednServer, BACKEND_SERVER_IP)
    # create a while-while to listen to steamvr messages
    # CheckSteamVRLogs
    # if logs updated
    # send status to backed server
    # loop



if __name__ == '__main__':
    #set host='0.0.0.0', port=80 to enable external access in local network
    # app.debug = True
    # app.use_reloader=False
    main()
    app.run(host='0.0.0.0', port=8080)

# , use_reloader=False
