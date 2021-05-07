import os
import glob
import json
import subprocess
file_dir = "C:\Program Files (x86)\Steam\steamapps\*.acf"
List = []
type = '.acf'

# '228980' SteamWorks
# '250820' SteamVR
# '410570' GunJack
# '450390' The LAb
# '826480' VR GirlFriend
#  file example: manifest_xxxxxx.acf

# Check the current installed non Steam application
def CheckInstalledNonSteamApplication(applist):
    with open('GamingServer/appdict.json') as f:
        data = json.load(f)
    for json_dict in data:
        if os.path.exists(json_dict['Address']):
            applist.append(json_dict['ID'])
            print(json_dict['Address'], 'exist')
        else:
            print(json_dict['Address'], 'does not exist')

# Check the current installed Steam game
def CheckInstalledSteamGame(applist):
    # with open('SteamAppList.json',newline='') as jsonfile:
    #     json_data = json.loads(jsonfile)
    for file in glob.glob(file_dir):
        str = os.path.basename(file)
        str = str[12:].replace(type,'')
        # '228980' SteamWorks # '250820' SteamVR
        if str != '228980' and str != '250820':
            # if json_data['applist']['apps']['appid'] == str
            #     print game(game['name'])
            applist.append(str)

# applist = list()
# CheckInstalledSteamGame(applist)
# CheckInstalledNonSteamApplication(applist)
# print(applist)