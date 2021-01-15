import sys
import time
import ctypes
import openvr

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
print(result , " ", openvr.getVRInitErrorAsSymbol(result))
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
    print("CloudXR_Server_State ", vr_sys.getInt32TrackedDeviceProperty(openvr.k_unTrackedDeviceIndex_Hmd, 10100))
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
    print(driver, display)

# print("2")
# print(openvr.getRuntimePath())
# print("3", vr_system.getRecommendedRenderTargetSize())
# print("4", vr_system.isDisplayOnDesktop())
print("End")
# for i in range(10):
#     xform = vr_system.getEyeToHeadTransform(openvr.Eye_Left)
#     print(xform)
#     sys.stdout.flush()
#     time.sleep(0.2)
