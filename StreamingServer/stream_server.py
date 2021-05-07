#stream_server.py
import subprocess
import multiprocessing
import nginx_manger
import requests
import psutil
import socket
from flask import Flask, request
stream_id = ''

app = Flask(__name__)


@app.route('/StartNginX', methods=['POST'])
def StartNginX():
    print("StartNginX")
    # multiprocessing.call(r'C:\livestream\start_nginx.bat', shell=True)
    nginx_manger.call()
    return 'StartNginX!'


@app.route('/StopNginX', methods=['POST'])
def StopNginX():
    print("StopNginX")
    nginx_manger.stop()
    # stop nginx by batch file
    return 'StopNginX!'


@app.route('/ReloadNginX', methods=['POST'])
def ReloadNginX():
    print("ReloadNginX")
    nginx_manger.reload()
    return 'ReloadNginX!'


@app.route('/CheckNginX', methods=['POST'])
def CheckNginX():
    print("CheckNginX")
    PROCNAME = "NGINX.exe"
    for proc in psutil.process_iter():
        if proc.name() == PROCNAME:
            print(proc.status())
            return proc.status()

    return "none"
    # "nginx" in (p.name() for p in psutil.process_iter())


@app.route('/start_streaming', methods=['POST'])
def start_streaming():
    global stream_id
    game_server_ip = request.form.get('game_server_ip', type=str)
    client_ip = request.form.get('client_ip', type=str)
    backend_server_ip = request.form.get('backend_server_ip', type=str)
    stream_server_ip = socket.gethostbyname(socket.gethostname())
    data = {
        'game_server_ip': game_server_ip,
        'client_ip': client_ip,
        'video_source_url': "/tmp_hls/stream/index.m3u8"
    }
    url = 'http://' + backend_server_ip + '/streaming'
    print(url)
    r = requests.post(url, data=data).json()
    # print('status: ', r['status'])
    # print('msg: ',r['msg'])
    # print('stream_id', r['stream_id'])
    stream_id = r['stream_id']
    # print('r.url :', r.url)
    # print('r.text : ', r.text)
    return "start streaming"
    # game server ip
    # client ip
    # response is stream id from backend


@app.route('/stop_streaming', methods=['POST'])
def stop_streaming():
    backend_server_ip = request.form.get('backend_server_ip', type=str)
    global stream_id
    print('stop streaming: ', stream_id)
    url = 'http://' + backend_server_ip + '/streaming/' + str(stream_id)
    requests.delete(url)
    print("stop streaming session")
    # send request to backend
    return "stop streaming"


def main():
    nginx_manger.call()


if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0', port=5000)
