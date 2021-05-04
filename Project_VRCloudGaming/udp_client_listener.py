import subprocess
import os

proc = ''
dir_path = os.path.dirname(os.path.realpath(__file__))
def start_udp_server():
    global proc
    proc = subprocess.Popen([dir_path+'/vJoyClient'])
    #if success:
        #return success
    #else:
        #return error
    # os.system("Project_VRCloudGaming/UDPReceiver")
def stop_udp_server():
    global proc
    proc.terminate()
    #if success:
        #return success
    #else:
        #return error
# start_udp_server()
