import asyncio
import ctypes
import os
import openvr
import sys
import subprocess
# import multiprocess as mp
from multiprocessing import Process
import time
import threading
import logging
import win32gui
import json
from enum import Enum
import backendManager as bm
#
print('openvr path: ',openvr.__path__)
#COMMAND
COMMAND_LAUNCH = 'start steam://rungameid/{0}'
COMMAND_CLOSE = 'taskkill /F /FI "IMAGENAME eq {0}*"'
g_CurrentAppTitle =''
logging.basicConfig(level=logging.DEBUG)
loop = asyncio.get_event_loop()

class ServerState(Enum):
    #Initial state
    ServerState_NotRunning = 0
    #Server is connecting to client, finished the RTSP handshake.
    ServerState_Connecting = 1
    #Server is ready to accept video and audio input for streaming
    ServerState_Running = 2
    #Server state when HMD is active. This is specific to VR mode.
    ServerState_HMD_Active = 3
    #Server state when HMD is idle. This is specific to VR mode.
    ServerState_HMD_Idle = 4
    #Server is disconnected from the client.
    ServerState_Disconnected = 5
    #Server in an error state.
    ServerState_Error = 6

def enumHandler(hwnd, lParam):
    if win32gui.IsWindowVisible(hwnd):
        if lParam in win32gui.GetWindowText(hwnd):
            # win32gui.MoveWindow(hwnd, 0, 0, 760, 500, True)
            win32gui.SetForegroundWindow(hwnd)

def CheckGameStatus(imagename):
    imagename = imagename +".exe"
    # p = os.popen('tasklist /FI "IMAGENAME eq %s"' % imagename)
    # return p.read().count(imagename)
    p = os.popen('tasklist /FI "IMAGENAME eq %s"' % imagename)
    pp = p.read().title()
    return pp.count(imagename.title())

def openGame(dict):
    BACKEND_SERVER_IP  = dict['BACKEND_SERVER_IP']
    player_ip = dict['player_ip']
    app_id = dict['app_id']
    app_title = dict['app_title']
    platform = dict['platform']
    timeout = 120
    period = 3
    time_count = 0
    mustend = time.time() + timeout
    isGameOpened = False
    while time.time() < mustend:
        if checkSteamVRInit() == 0: #CloudXR Connect Success
            if platform == 'steam':
                os.system(COMMAND_LAUNCH.format(app_id))
            elif platform == 'compal':
                startApplication(app_title, app_id)
            while CheckGameStatus(app_title) == 0 :
                continue
            isGameOpened = True
            #move the game application to foreground
            # win32gui.EnumWindows(enumHandler,app_title)
            print("start game success!")
            break
        else:
            time_count += period
            # logging.info("wait for connecting: ", time_count, ' seconds')
            print("wait for connecting : ", time_count)
            time.sleep(period)
    if isGameOpened == True:
        print("playing")
        bm.SendGameConnection(BACKEND_SERVER_IP,player_ip, app_id, "playing",platform)
    else:
        print("timeout")
        bm.SendGameConnection(BACKEND_SERVER_IP,player_ip, app_id, "timeout",platform)
    return True

def startSteamvr(app_id):
    os.system(COMMAND_LAUNCH.format(app_id))

def startGame(BACKEND_SERVER_IP,player_ip, app_id, app_title, platform):
    print("=========startGame1===========")
    dict = {'BACKEND_SERVER_IP' : BACKEND_SERVER_IP, 'player_ip': player_ip,
    'app_id': app_id, 'app_title' : app_title, 'platform' : platform}
    global p
    p = Process(target = openGame, args=(dict,))
    p.start()
    # p.join()
    print("=========startGame2===========")
    # p.join()

def startApplication(app_title, app_id):
    with open('Project_VRCloudGaming/appdict.json') as f:
        data = json.load(f)
    for json_dict in data:
        if app_id == json_dict['ID']:
            os.startfile(json_dict['Address'])
            print(json_dict['Address'])

def start_game_asyncio(BACKEND_SERVER_IP,player_ip, app_id):
    # dict = {'BACKEND_SERVER_IP' : BACKEND_SERVER_IP, 'player_ip': player_ip,
    # 'app_id': app_id}
    print("start_game_asyncio")

def timeoutOpenGame(BACKEND_SERVER_IP):
    global p
    if p.is_alive():
        p.terminate()
        bm.SendGameTimeout(BACKEND_SERVER_IP)

def closeGame(app_title):
    os.system(COMMAND_CLOSE.format(app_title))

def setAppID(app_id):
    global g_CurrentAppID
    g_CurrentAppID = app_id

def getAppID():
    return g_CurrentAppID

def setAppTitle(app_title):
    global g_CurrentAppTitle
    g_CurrentAppTitle = app_title

def getAppTitle():
    return g_CurrentAppTitle

def checkSteamVRInit():
    result = openvr.checkInitError(openvr.VRApplication_Background)
    # print("result: " , result)
    # print("result As Symbol: ", openvr.getVRInitErrorAsSymbol(result))
    return result

def printSteamVRInfo():
    print("OpenVR test program")

    if openvr.isHmdPresent():
        print("VR head set found")

    if openvr.isRuntimeInstalled():
        print("Runtime is installed")
        print(openvr.runtimePath())

    #To initialize the API and get access to the vr::IVRSystem interface call the vr::VR_Init function
    # VRApplication_Background
    # VRApplication_Utility : IVRSettings and IVRApplications are guaranteed to work
    result = openvr.checkInitError(openvr.VRApplication_Background)
    print("test" , result , " ", openvr.getVRInitErrorAsSymbol(result))
    if result == 0:
        state = 10100
    #-------------------------------------------------------------
    #Developing part

    vr_app = openvr.IVRApplications()
    #ctypes.c_char_p("410570")
    print("vr_app getApplicationState: ", vr_app.getApplicationState())
    print("vr_app getTransitionState: ", vr_app.getApplicationsTransitionStateNameFromEnum(vr_app.getTransitionState()))
    print("vr_app : " ,vr_app.getApplicationProcessId('SteamVR.exe'.encode("utf-8")))
    # vr_settings = openvr.VRSettings()
    if result == 0:
        vr_sys = openvr.VRSystem()
        state = vr_sys.getInt32TrackedDeviceProperty(openvr.k_unTrackedDeviceIndex_Hmd, 10100)
        print("CloudXR_Server_State ", ServerState(ctypes.c_ulong(state[0]).value).name)
        print("isDisplayOnDesktop ", vr_sys.isDisplayOnDesktop())
        print("isTrackedDeviceConnected ", vr_sys.isTrackedDeviceConnected(openvr.k_unTrackedDeviceIndex_Hmd))
        # print("getPropErrorNameFromEnum ", vr_sys.getPropErrorNameFromEnum(result))
        driver = vr_sys.getStringTrackedDeviceProperty(
                    openvr.k_unTrackedDeviceIndex_Hmd,
                    openvr.Prop_TrackingSystemName_String,
                )
        display = vr_sys.getStringTrackedDeviceProperty(
                    openvr.k_unTrackedDeviceIndex_Hmd,
                    openvr.Prop_SerialNumber_String,
                )
        print("driver: ", driver, "; diplay :", display)
    # for i in range(10):
    #     xform = vr_system.getEyeToHeadTransform(openvr.Eye_Left)
    #     print(xform)
    #     sys.stdout.flush()
    #     time.sleep(0.2)

# checkSteamVRInit()
