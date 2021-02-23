import subprocess
import socket
import requests
from multiprocessing import Process

def start(backend_server_ip, stream_server_ip, client_ip):
    local_ip = socket.gethostbyname(socket.gethostname())
    data = {
        'game_server_ip': local_ip,
        'client_ip': client_ip,
        'backend_server_ip': backend_server_ip
    }

    url = 'http://' + stream_server_ip + '/start_streaming'
    r = requests.post(url, data=data)

    subprocess.Popen(
        r'C:\Users\AlexTY_Liu\Documents\GitHub\CompalGit\Project_VRCloudGaming\obs_start_streaming.bat',
        shell=True)
    print('r.url :', r.url)
    print('r.text : ', r.text)
    return True

def stop(backend_server_ip, stream_server_ip):
    data = {'backend_server_ip': backend_server_ip}
    url = 'http://' + stream_server_ip + '/stop_streaming'
    requests.post(url, data=data)
    subprocess.Popen(
        r'C:\Users\AlexTY_Liu\Documents\GitHub\CompalGit\Project_VRCloudGaming\obs_stop_streaming.bat',
        shell=True)
    return True
