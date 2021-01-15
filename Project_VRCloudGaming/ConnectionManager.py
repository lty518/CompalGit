# ConnectionManager
import requests


def SendGameConnection(client_ip, game_ip, connection_status):
    data = {'client_ip': client_ip, 'game_ip': game_ip,
            'connection_status': connection_status}

    server_ip = '172.16.0.189:5000'
    url = 'http://' + server_ip +'/connection-status'
    r = requests.post(url, data=data)
    # r = requests.post('http://172.16.0.189:5000/connection-status', data=data)
    # r = requests.get('http://127.0.0.1:8080/', params = my_data)
    # And done.
    print(r.url)
    print(r.text)  # displays the result body.

""" Uncomment below to debug"""
# SendGameConnection("123","456","0")
