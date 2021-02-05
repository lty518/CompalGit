# Send a string to Logitech Touch Mouse server:
# www.logitech.com/support/6367

import socket

IP ='172.16.0.3'
PORT = 54000
BUFFER = 64
MESSAGE = 'iTouchOSX'
print('server IP:',IP,'port:',PORT)

def closeout():
    sTCP.close()
    sUDP.close()
    print ('Disconnected')
    
def sendchar(): 
    inputString = raw_input("> Enter text: ")
    #print 'Input:',inputString

    if inputString == '?ESC':
        closeout();
    else:
        
        for letter in inputString:
            #print 'Char:',letter
            hexPrefix = '0000000d000000'
            hexChar = letter.encode('hex')
            toJoin = [hexPrefix, hexChar]
            hexData = "".join(toJoin)
            PACKETDATA = hexData.decode('hex')
            sUDP.send(PACKETDATA)
        else:
            sendchar();

print( "opening TCP socket..")
try:
    sTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print( "done.")
except socket.error, msg:
    print ('failed.')
    exit()

print ('connecting to Touch Mouse Server..')
try:    
    sTCP.connect((IP, PORT))
except socket.error.msg:
    print ('connection refused. Is Touch Mouse Server running?')
    exit()

data = sTCP.recv(BUFFER)
print ('ACK:',data,)

if data == MESSAGE:
    print ('- server ready!')
