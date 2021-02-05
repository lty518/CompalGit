import requests
my_data = {'game-title': 'GunJack', 'game_id' : '410570',
           'player_ip': '172.16.0.213'}
r = requests.post("http://172.16.0.3:8080/game-connection/", my_data)
#And done.
print(r.text)
