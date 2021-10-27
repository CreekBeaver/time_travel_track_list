import requests
import json

url = 'http://localhost:9115/'
data = {'name': 'advil'}
jsonData = json.dumps(data)
r = requests.post(url=url, json=jsonData)

d = r.json()
print(d)