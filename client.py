import requests
import json

url = 'http://localhost:9115/'
data = {'key' : 'Value', "key2" : "value2"}
jsonData = json.dumps(data)
r = requests.post(url=url, json=jsonData)

d = r.json()
print(d)
print(d['name'])