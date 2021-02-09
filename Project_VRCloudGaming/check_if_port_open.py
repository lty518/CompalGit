import socket

def check(IP, Port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (IP, Port)
    result_of_check = a_socket.connect_ex(location)

    if result_of_check == 0:
       print("Address: ", IP, ":", Port, "is open")
    else:
       print("Address: ", IP, ":", Port, "is not open")
    a_socket.close()

def tryPort(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        sock.bind(("0.0.0.0", port))
        print("Port is not in use")
        result = True
    except:
        print("Port is in use")
    sock.close()
    return result

tryPort(5037)
