import socket
import systemSettings
def getLocalIP():
    local_ip = socket.gethostbyname(socket.gethostname())
    print("local_ip: ", local_ip)
    systemSettings.set('LOCAL_IP',local_ip)
    return local_ip
    # fp = open("local_ip.txt",'w')
    # fp.write(local_ip)
    # fp.close()

# getLocalIP()
