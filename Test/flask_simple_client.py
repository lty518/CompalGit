import requests
my_data = {'key1': 'value1', 'key2': 'value2', 'foo' : 'bar'}
r = requests.post('http://127.0.0.1:8080/', data = my_data)
# r = requests.get('http://127.0.0.1:8080/', params = my_data)
# And done.
print(r.url)
print(r.text) # displays the result body.

# import requests
# my_data = {'game-title': 'GunJack', 'game_id' : '410570',
#            'player_ip': '172.16.0.213'}
# r = requests.post("http://172.16.0.3:8080/game-connection/", my_data)
# #And done.
# print(r.text)