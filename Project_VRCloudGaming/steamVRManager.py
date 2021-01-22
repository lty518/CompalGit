import asyncio
import ctypes
import os
import openvr
import sys
import subprocess
import multiprocess as mp
import time
import threading
import logging
from enum import Enum
import backendManager as bm
#COMMAND
COMMAND_LAUNCH = 'start steam://rungameid/{0}'
# COMMAND_CLOSE = 'taskkill /FI "WINDOWTITLE eq "{0}"'
COMMAND_CLOSE = 'taskkill /F /FI "IMAGENAME eq {0}*"'
g_CurrentGameTitle =''
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
    game_id = dict['game_id']
    game_title = dict['game_title']
    timeout = 120
    period = 3
    time_count = 0
    mustend = time.time() + timeout
    isGameOpened = False
    while time.time() < mustend:
        if checkSteamVRInit() == 0:
            os.system(COMMAND_LAUNCH.format(game_id))
            while CheckGameStatus(game_title) == 0 :
                continue
            isGameOpened = True
            print("start game success!")
            break
        else:
            time_count += period
            # logging.info("wait for connecting: ", time_count, ' seconds')
            print("wait for connecting : ", time_count)
            time.sleep(period)
    if isGameOpened == True:
        print("playing")
        bm.SendGameConnection(BACKEND_SERVER_IP,player_ip, game_id, "playing")
    else:
        print("timeout")
        bm.SendGameConnection(BACKEND_SERVER_IP,player_ip, game_id, "timeout")
    return True

def startSteamvr(game_id):
    os.system(COMMAND_LAUNCH.format(game_id))

def startGame(BACKEND_SERVER_IP,player_ip, game_id, game_title):
    print("=========startGame1===========")
    dict = {'BACKEND_SERVER_IP' : BACKEND_SERVER_IP, 'player_ip': player_ip,
    'game_id': game_id, 'game_title' : game_title}
    p = mp.Process(target = openGame, args=(dict,))
    p.start()
    print("=========startGame2===========")
    # p.join()

def start_game_asyncio(BACKEND_SERVER_IP,player_ip, game_id):
    dict = {'BACKEND_SERVER_IP' : BACKEND_SERVER_IP, 'player_ip': player_ip,
    'game_id': game_id}



def closeGame(game_title):
    os.system(COMMAND_CLOSE.format(game_title))

def setGameID(game_id):
    global g_CurrentGameID
    g_CurrentGameID = game_id

def getGameID():
    return g_CurrentGameID

def setGameTitle(game_title):
    global g_CurrentGameTitle
    g_CurrentGameTitle = game_title

def getGameTitle():
    return g_CurrentGameTitle

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
