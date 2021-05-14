import requests
my_params = {'key1': 'value1', 'key2': 'value2'}
r = requests.get('https://www.google.com.tw/')
r = requests.get('http://httpbin.org/get', params = my_params)
# And done.
print(r.text) # displays the result body.
print(r.url)
if r.status_code == requests.codes.ok:
  print("OK")
