import os
import json
import subprocess
# file_path = os.path.relpath('GamingServer/appdict.json')
# with open(os.path.relpath('GamingServer/appdict.json')) as f:
#     data = json.load(f)
# for json_dict in data:
#     print(json_dict['Address'])
# print (os.path.relpath('\GamingServer\Script\start_steamvr.bat'))
# subprocess.Popen(r'\GamingServer\Script\close_steamvr.bat', shell=True)

# with open(os.path.relpath('GamingServer/appdict.json')) as f:
#     data = json.load(f)
# for json_dict in data:
#     if json_dict['ID'] == '3':
#         path = json_dict['DroidCam_Path']
#         # path = r'C:\Program Files (x86)\DroidCam\DroidCamApp.exe'
#         subprocess.Popen([ path, '-c', '172.16.0.54', '4747', '-video'])
#         while 1:
#             continue
g_CurrentApplication = 'DroidCamApp.exe'
COMMAND_CLOSE = 'taskkill /F /FI "IMAGENAME eq {0}*"'
os.system(COMMAND_CLOSE.format(g_CurrentApplication))
