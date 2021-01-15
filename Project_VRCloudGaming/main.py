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
import get_local_IP
import yaml
from os import path
#-----------------------------
from check_installed_game import CheckInstalledGame
from connection_manager import SendGameConnection
app = Flask(__name__)

#GAME_ID
TEAMVR_GAMEID = '250820'
HELLBLADE = '747350'
STEAMVR_ID = '250820'
#GAME_NAME
SteamVR = 'vrserver'
GUNJACK = 'Gunjack'
#COMMAND
COMMAND_LAUNCH = 'start steam://rungameid/{0}'
COMMAND_CLOSE = 'taskkill /FI "WINDOWTITLE eq "{0}"'
#IP
#Acer notebook  172.16.0.189
#hp notebook 172.16.0.3
#Jared Backend 172.16.0.25
CLOUDXR_SERVER_MANAGER_IP = '172.16.0.189' #Acer notebook
CLOUDXR_CLIENT_IP = '172.16.0.213' #Oculus Quest
BACKEND_SERVER_IP = '172.16.0.189'
#FLAG
is_available = 1
game_title = ''
player_ip = ''

#GlOBAL VARIABLES
launch_time = time.time()
g_CurrentGameID = ''

# Register to manager
def RegisterToBackednServer(backend_ip):
    if os.path.isfile('local_ip.txt') == False:
        getLocalIP()
    f = open("local_ip.txt",'r')
    local_ip = f.read()
    data = {'edge_ip': local_ip}
    try:
        r = post('http://{0}:5000//register'.format(backend_ip), data= data)
        print ("register_to_backend_server" + r.text)
    except exceptions.RequestException as e:
        raise SystemExit(e)

def UnregisterToBackednServer():
    res = get('http://{0}:5000/deregister'.format(backend_ip))
    print(res.text)

def CheckGameStatus(imagename):
    imagename = imagename +".exe"
    p = os.popen('tasklist /FI "IMAGENAME eq %s"' % imagename)
    return p.read().count(imagename)

def open_game(game_id):
    os.system(COMMAND_LAUNCH.format(game_id))

def close_game(game_id):
    os.system(COMMAND_CLOSE.format(game_id))

@app.route('/')
def hello():
    return "<h1>Hello World!</h1>"

@app.route("/hello/<text>")
def index(text):
    print(text)
    return "<h1>%s</h1>" % text

#check if steamvr is ok and return ready for a user to connect
@app.route('/game-connection', methods=['POST', 'GET'])
def launch_cloudxr():
    if request.method == 'POST':
        global player_ip, is_available, g_CurrentGameID, game_title
        # if not is_available:
        #     return 'Game server not available now'
        game_title = request.form.get('game_title', type=str)
        game_id = request.form.get('game_id', type=str)
        player_ip = request.form.get('player_ip', type=str)
        g_CurrentGameID = game_id
        print("request: ", game_title, game_id, player_ip)
        # Game_id needs to be generalized
        # if os.system(COMMAND_LAUNCH.format(sTEAMVR_GAMEID)) == 0:
        # if os.system(COMMAND_LAUNCH.format(HELLBLADE)) == 0:
        if CheckGameStatus(SteamVR) >= 1:
            is_available = 0
            print('Available: ', is_available)
            open_game(game_id)
            SendGameConnection(player_ip, game_id, "playing")
            return {'launch success': True}
        else:
            return {'launch success': False}
    # for launching steamVR process
    else:
        if time.time() > launch_time+10:
            return {'status': True}
        else:
            return {'status': False}


@app.route('/game-disconnection', methods=['POST'])
def close_clourdxr():
    global player_ip, is_available, g_CurrentGameID, game_id, game_title
    print(player_ip, request.remote_addr)
    game_id = request.form.get('game_id', type=str)
    game_title = request.form.get('game_title', type=str)
    # if request.remote_addr != player_ip and player_ip != '127.0.0.1':
    #     return 'Invalid request'
    # Close game app and steamVR, and reset game server status
    if CheckGameStatus(game_title) >= 1:
        close_game(game_title)
        g_CurrentGameID = ''
        player_ip = ''
        is_available = 1
        print(player_ip, is_available)
        SendGameConnection(player_ip, game_id, "closed")
        # RegisterToBackednServer()
        return {'close success': True, 'game_title' : game_title}
    else:
        return {'close success': False, 'game_title' : game_title}


@app.route('/stream-info')
def get_stream_info():
    return 'Under construction'

@app.route('/steamvr-status', methods=['POST', 'GET'])
def get_steamvr_status():
    if CheckGameStatus(SteamVR) >= 1:
        return {'SteamVR Status': True}
    else:
        return {'SteamVR Status': False}

@app.route('/game-status', methods=['POST', 'GET'])
def get_game_status():
    game_id = request.form.get('game_id', type=str)
    game_title = request.form.get('game_title', type=str)
    if CheckGameStatus(game_title) >= 1:
        return {'game_id Status': True, 'game_title' : game_title}
    else:
        return {'game_id Status': False, 'game_title' : game_title}

def main():
    # program start
    # check installed steamvr games in pc
    list = CheckInstalledGame()
    global BACKEND_SERVER_IP
    # with open("Settings.yaml",'r') as stream:
    #
    # with open("system_settings.yaml", 'r') as stream:
    #     settings = yaml.load(stream)
    # register to backed server
    RegisterToBackednServer(BACKEND_SERVER_IP)
    #if steamVR not open
    if CheckGameStatus(SteamVR) == 0:
        print ("SteamVR is not running, open now!")
        open_game(STEAMVR_ID)
        while CheckGameStatus(SteamVR) == 0 :
            continue
    else:
        print("SteamVR is running!")

    # create a while-while to listen to steamvr messages
    # CheckSteamVRLogs
    # if logs updated
    # send status to backed server
    # loop
    atexit.register(UnregisterToBackednServer)

main()

if __name__ == '__main__':
    #set host='0.0.0.0', port=80 to enable external access in local network
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
