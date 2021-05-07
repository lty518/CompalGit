import subprocess
import multiprocessing as mp
from subprocess import Popen

def start():
    subprocess.call(r'C:\livestream\start_nginx.bat', shell=True)

def stop():
    subprocess.call(r'C:\livestream\stop_nginx.bat', shell=True)

def reload():
    subprocess.call(r'C:\livestream\reload_nginx.bat', shell=True)

def check():
    print("check stream source")

def call():
    ap = mp.Process(target=start)
    ap.start()
    ap.join()

