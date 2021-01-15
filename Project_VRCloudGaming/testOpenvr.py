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
vr_app = openvr.IVRApplications()
print("vr_app : " ,vr_app.getApplicationProcessId(ctypes.c_char_p("410570")))
# vr_settings = openvr.VRSettings()
if result == 0:
    vr_sys = openvr.VRSystem()
    driver = vr_sys.getStringTrackedDeviceProperty(
                openvr.k_unTrackedDeviceIndex_Hmd,
                openvr.Prop_TrackingSystemName_String,
            )
    display = vr_sys.getStringTrackedDeviceProperty(
                openvr.k_unTrackedDeviceIndex_Hmd,
                openvr.Prop_SerialNumber_String,
            )
    print(driver)
    print(display)

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
