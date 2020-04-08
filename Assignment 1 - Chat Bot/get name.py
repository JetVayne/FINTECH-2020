import requests
from bs4 import BeautifulSoup as soup

url = 'https://www.twse.com.tw/zh/brokerService/brokerServiceAudit'
res = requests.get(url)
html = res.text.replace('\xa0', '')
doc = soup(html, 'html.parser')

table = doc.select('table.grid > tbody > tr')

for i in table:
    print(i.select('td')[1].select('a')[0].text)
    # break


