import os
import glob
file_dir = "C:\Program Files (x86)\Steam\steamapps\*.acf"
List = []
type = '.acf'

# '228980' SteamWorks
# '250820' SteamVR
# '410570' GunJack
# '450390' The LAb
# '826480' VR GirlFriend
#  file example: manifest_xxxxxx.acf

def CheckInstalledGame():
    # with open('SteamAppList.json',newline='') as jsonfile:
    #     json_data = json.loads(jsonfile)
    for file in glob.glob(file_dir):
        str = os.path.basename(file)
        str = str[12:].replace(type,'')
        # '228980' SteamWorks # '250820' SteamVR
        if str != '228980' and str != '250820':
            # if json_data['applist']['apps']['appid'] == str
            #     print game(game['name'])
            List.append(str)
    print(List)
    return List

# CheckInstalledGame()
