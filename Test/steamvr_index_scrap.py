import requests
from bs4 import BeautifulSoup


url = 'http://localhost:27062/console/index.html'
thepage = requests.get(url)
print (thepage.status_code)
str = thepage.text
# print(str.encode("utf-8").decode("cp950","ignore")) #layout in order
# print(thepage.content)# not layout in order
urlsoup = BeautifulSoup(thepage.text, "lxml") #default use html.parser

for div in urlsoup.findAll('div'):
    for c in div.children:
        c_text = c.text
        print(c_text.encode("utf-8").decode("cp950","ignore"))
for team in urlsoup.findAll(class_='row logname'):
    print (team.text)

sel = urlsoup.select("div.row") #取HTML標中的 <div class="title"></div> 中的<a>標籤存入sel
for s in sel:
    print( s.data)
# html = list(urlsoup.children)[2]
# body = list(html.children)[3]
# str = urlsoup.prettify()
# print(str.encode("utf-8").decode("cp950","ignore"))
