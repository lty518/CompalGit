import socket

def getLocalIP():
    local_ip = socket.gethostbyname(socket.gethostname())
    fp = open("local_ip.txt",'w')
    fp.write(local_ip)
    fp.close()
