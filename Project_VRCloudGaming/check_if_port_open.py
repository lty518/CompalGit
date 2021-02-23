import socket


def check(IP, Port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (IP, Port)
    result_of_check = a_socket.connect_ex(location)
    a_socket.close()
    if result_of_check == 0:
        print("Address: ", IP, ":", Port, "is in use")
        return "Address: " + IP + ":" + Port + "is in use"
    else:
        print("Address: ", IP, ":", Port, "is not in use")
        return "Address: " + IP + ":" + Port + "is not in use"


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

# tryPort(5037)
