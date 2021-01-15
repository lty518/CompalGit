#flask_simple_server
import os
import glob
import atexit
from requests import get, post, exceptions
from flask import Flask, request
import time
from threading import Timer
#-----------------------------
from CheckInstalledGame import CheckInstalledGame

app = Flask(__name__)

teamVR_gameid = '250820'
hellblade = '747350'
launch_cmd = 'start steam://rungameid/{0}'
close_cmd = 'taskkill /IM "{0}" /F'
CLOUDXR_SERVER_MANAGER_IP = '172.16.0.189' #Acer notebook
# # game_server_manager_ip = '192.168.0.103'
is_available = 1
player_ip = ''
launch_time = time.time()

# Register to manager
def RegisterToBackednServer():
    try:
        r = post('http://{0}:5000//register'.format(CLOUDXR_SERVER_MANAGER_IP))
        print ("register_to_backend_server" + r.text)
    except exceptions.RequestException as e:
        raise SystemExit(e)

def UnregisterToBackednServer():
    res = get('http://{0}:5000/deregister'.format(CLOUDXR_SERVER_MANAGER_IP))
    print(res.text)


#
#
# def open_game():
#     os.system(launch_cmd.format(hellblade))
#
#

# program start
# check installed steamvr games in pc
list = CheckInstalledGame()
# register to backed server
RegisterToBackednServer()
# create a while-while to listen to steamvr messages
# CheckSteamVRLogs
# if logs updated
# send status to backed server
# loop

atexit.register(UnregisterToBackednServer)

@app.route('/')
def hello():
    return "<h1>Hello World!</h1>"

@app.route("/hello/<text>")
def index(text):
    print(text)
    return "<h1>%s</h1>" % text
    # return "<h1>Hello, %s</h1>" % text

@app.route('/', methods=['POST'])
def result():
    print(request.form['foo']) # should display 'bar'
    return 'Received !' # response to your request.



# @app.route('/game-connection', methods=['POST', 'GET'])
# def launch_cloudxr():
#     global launch_time
#     if request.method == 'POST':
#         global player_ip, is_available
#         if not is_available:
#             return 'Game server not available now'
#         game_title = request.form.get('game_title', type=str)
#         game_id = request.form.get('game_id', type=str)
#         player_ip = request.form.get('player_ip', type=str)
#         print(game_title, game_id, player_ip)
#         # Game_id needs to be generalized
#         # if os.system(launch_cmd.format(steamVR_gameid)) == 0:
#         # if os.system(launch_cmd.format(hellblade)) == 0:
#         if is_available:
#             is_available = 0
#             print('Available: ', is_available)
#             t = Timer(10, open_game)
#             launch_time = time.time()
#             t.start()
#             return {'launch success': True}
#         else:
#             return {'launch success': False}
#     # for launching steamVR process
#     else:
#         if time.time() > launch_time+10:
#             return {'status': True}
#         else:
#             return {'status': False}
#
#
# @app.route('/game-disconnection', methods=['POST'])
# def close_clourdxr():
#     global player_ip, is_available
#     print(player_ip, request.remote_addr)
#     if request.remote_addr != player_ip and player_ip != '127.0.0.1':
#         return 'Invalid request'
#     # Close game app and steamVR, and reset game server status
#     if os.system(close_cmd.format("vrmonitor.exe")) == 0:
#         player_ip = ''
#         is_available = 1
#         print(player_ip, is_available)
#         RegisterToBackednServer()
#         return {'close success': True}
#     else:
#         return {'close success': False}
#
#
# @app.route('/stream-info')
# def get_stream_info():
#     return 'Under construction'

if __name__ == '__main__':
    #set host='0.0.0.0', port=80 to enable external access in local network
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
