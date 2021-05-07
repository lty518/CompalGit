# Gaming Server
***
# 環境設定
1. Python 環境及套件安裝
    * 安裝Python 3
    * 安裝套件
    * 修改Python OpenVR，在裡面增加CheckInitError()
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
兩種方法
1. 執行 start_gameserver.bat
2. 透過python 執行main.py





