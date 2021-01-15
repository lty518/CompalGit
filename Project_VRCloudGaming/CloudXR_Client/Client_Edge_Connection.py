
import requests
my_data = {'game_title': "GunJack",
           'game_id': "410570", 'player_ip': "172.16.0.213"}
# '410570' GunJack
# '450390' The LAb
# '826480' VR GirlFriend


def Launch_CloudXR_Server_Game():
    # if cloudxr connection is ready thean launch game

    # check game id

    # launch game
    r = requests.post('http://127.0.0.1:8080/game-connection', data=my_data)
    print(r.url)
    print(r.text)
def Shutdown_CloudXR_Server_Game():
    # if cloudxr connection is ready thean launch game

    # check game id

    # launch game
    r = requests.post('http://127.0.0.1:8080/game-disconnection', data=my_data)
    print(r.url)
    print(r.text)

Shutdown_CloudXR_Server_Game()
# Launch_CloudXR_Server_Game()
