import socket
import threading
import msvcrt
import time

from pynput import keyboard

dest_ip = '192.168.45.87' #172.16.0.3
dest_port = int(8001)#54000 7890
# 1. 建立套接字
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 2. 繫結本地資訊
udp_socket.bind(("", 7890))
def on_key_press(key):
    global udp_socket
    try:
        msg = transkey(b'KeyDown,' , key.char)
        if transkey(b'KeyDown,',key.char) != b'KeyDown,'+b'0':
            udp_socket.sendto(msg, (dest_ip, dest_port))
        print(msg)
    except AttributeError:
        msg = transkey(b'KeyDown,' , str(key))
    

def on_key_release(key):
    global udp_socket
    try:
        msg = transkey(b'KeyUp,', key.char)
        if transkey(b'KeyUp,', key.char) != b'KeyUp,'+b'0':
            udp_socket.sendto(msg, (dest_ip, dest_port))
        print(msg)
    except AttributeError:
        msg = transkey(b'KeyUp,', str(key))

def transkey(state, keyboard_input):
    if keyboard_input == 'w':
        if state == b'KeyDown,':
            return b'AxisTouch,16,1'
        else:
            return b'AxisTouch,16,0'
    elif keyboard_input == 's':
        if state == b'KeyDown,':
            return b'AxisTouch,16,-1'
        else:
            return b'AxisTouch,16,0'
    elif keyboard_input == 'a':
        if state == b'KeyDown,':
            return b'AxisTouch,15,-1'
        else:
            return b'AxisTouch,15,0'
    elif keyboard_input == 'd':
        if state == b'KeyDown,':
            return b'AxisTouch,15,1'
        else:
            return b'AxisTouch,15,0'
    elif keyboard_input == '1':
        if state == b'KeyDown,':
            return b'AxisTouch,1,-1'
        else:
            return b'AxisTouch,1,0'
    elif keyboard_input == '2':
        if state == b'KeyDown,':
            return b'AxisTouch,1,1'
        else:
            return b'AxisTouch,1,0'
    elif keyboard_input == '3':
        if state == b'KeyDown,':
            return b'AxisTouch,0,-1'
        else:
            return b'AxisTouch,0,0'
    elif keyboard_input == '4':
        if state == b'KeyDown,':
            return b'AxisTouch,0,1'
        else:
            return b'AxisTouch,0,0'
    elif keyboard_input == '5':
        if state == b'KeyDown,':
            return b'AxisTouch,11,-1'
        else:
            return b'AxisTouch,11,0'
    elif keyboard_input == '6':
        if state == b'KeyDown,':
            return b'AxisTouch,11,1'
        else:
            return b'AxisTouch,11,0'
    elif keyboard_input == '7':
        if state == b'KeyDown,':
            return b'AxisTouch,14,-1'
        else:
            return b'AxisTouch,14,0'
    elif keyboard_input == '8':
        if state == b'KeyDown,':
            return b'AxisTouch,14,1'
        else:
            return b'AxisTouch,14,0'
    elif keyboard_input == '9':
        if state == b'KeyDown,':
            return b'AxisTouch,17,1'
        else:
            return b'AxisTouch,17,0'
    elif keyboard_input == '0':
        if state == b'KeyDown,':
            return b'AxisTouch,18,1'
        else:
            return b'AxisTouch,18,0'
    elif keyboard_input == 'i':
        return state + b'100'#
    elif keyboard_input == 'k':
        return state + b'96'#
    elif keyboard_input == 'j':
        return state + b'99'#
    elif keyboard_input == 'l':
        return state + b'97'#
    elif keyboard_input == 'q':
        return state + b'106'#
    elif keyboard_input == 'e':
        return state + b'102'#
    elif keyboard_input == 'u':
        return state + b'107'#
    elif keyboard_input == 'o':
        return state + b'103'#
    elif keyboard_input == 'f':
        return state + b'109'
    elif keyboard_input == 'h':
        return state + b'108'
    else:
        return state + b'0'
        # return bytes(keyboard_input, 'utf-8')

def send_msg(udp_socket):
    keyboard_char = ''
    msg =b''
    while True:
        # 1. 從鍵盤輸入資料
        if msvcrt.kbhit():
            keyboard_char = msvcrt.getch()
            msg = transkey(b'KeyDown,', keyboard_char)           
            print ("Key pressed: ", keyboard_char, " send : ", msg)
            udp_socket.sendto(msg, (dest_ip, dest_port))



def recv_msg(udp_socket):
    """接收資料並顯示"""
    while True:
        # 1. 接收資料
        recv_msg = udp_socket.recvfrom(1024)
        # 2. 解碼
        recv_ip = recv_msg[1]
        recv_msg = recv_msg[0].decode("utf-8")
        # 3. 顯示接收到的資料
        print(">>>%s:%s" % (str(recv_ip), recv_msg))


def main():

    # 3. 建立一個子執行緒用來接收資料
    t = threading.Thread(target=recv_msg, args=(udp_socket,))
    t.start()

    # 4. 開啟鍵盤監聽用來傳送壓放按鍵的資訊
    with keyboard.Listener(on_press = on_key_press, on_release = on_key_release) as listener:
        listener.join()

    '''Legacy code'''
    # send_msg(udp_socket)



if __name__ == "__main__":
    main()