# Gaming Server
***
# 環境設定
1. Python 環境及套件安裝
    * 安裝Python 3
    * 安裝套件
```   
    pip install requests
    pip install sockets
    pip install logging
    pip install psutil
    pip install multiprocessing
    pip install GPUtil
    pip install flask
    pip install openvr
    pip install win32gui
    pip install enum
    pip install asyncio
```   
    * 修改Python OpenVR，在裡面增加CheckInitError()
    example path: 'C:\Users\AlexTY_Liu\AppData\Roaming\Python\Python39\site-packages'
```
_openvr.VR_InitInternal2.restype = c_uint32
_openvr.VR_InitInternal2.argtypes = [POINTER(EVRInitError), EVRApplicationType, c_char_p]
def checkInitError(eApplicationType, pStartupInfo=None):
    error = EVRInitError()
    result =     _openvr.VR_InitInternal2(byref(error), eApplicationType, pStartupInfo)
    return error.value
```    
2. SteamVR 安裝

3. OBS 及 OpenVR Plugin 安裝
    * https://obsproject.com/
    * https://github.com/baffler/OBS-OpenVR-Input-Plugin


# 運行Gaming Server
1. 首先必須先確保Backend Server是打開的
2. 接下來有兩種方法
    a. 執行 start_gameserver.bat (目前會遇到需要把checkInstalledGame.py ln18的GamingServer/拿掉才抓的到路徑，待修)
    b. 透過python 執行main.py





