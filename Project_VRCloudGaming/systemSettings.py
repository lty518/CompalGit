import os
import yaml


def write(new_yaml_data_dict):

    if not os.path.isfile("gamedict.yaml"):

        with open("gamedict.yaml", "a",encoding="utf-8") as fo:
            fo.write("---\n")

    #the leading spaces and indent=4 are key here!
    sdump = "  " + yaml.dump(
                new_yaml_data_dict
                ,indent=4
                )

    with open("gamedict.yaml", "a",encoding="utf-8") as fo:
        fo.write(sdump)

def AppendDict(game_id, game_title):
    d = {'game':{'game_id' : game_id, 'game_title' : game_title}}
    write(d)

def set(name, value):
    with open(os.getcwd()+'\Project_VRCloudGaming\system_settings.yaml',encoding="utf-8") as stream:
        data = yaml.load(stream, Loader=yaml.FullLoader)
    data[name] = value
    with open(os.getcwd()+'\Project_VRCloudGaming\system_settings.yaml','w',encoding="utf-8") as stream:
        yaml.dump(data, stream)

def loadConfig():
    print("=====loadSystemSettings=====")
    print("os.getcwd() :"os.getcwd())
    with open(os.getcwd()+'\Project_VRCloudGaming\system_settings.yaml', 'r') as stream:
        data = yaml.load(stream, Loader=yaml.FullLoader)
    # print(yaml.dump(data))
    print("CLOUDXR_SERVER_MANAGER_IP", data['CLOUDXR_SERVER_MANAGER_IP'])
    print("CLOUDXR_CLIENT_IP", data['CLOUDXR_CLIENT_IP'])
    print("BACKEND_SERVER_IP", data['BACKEND_SERVER_IP'])
    print("============================")
    return data

# set('LOCAL_IP', '172.16.0.3')
