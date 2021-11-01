import requests
import json

#url = 'http://localhost:9115/'
url = 'https://young-shore-84821.herokuapp.com/'
data = {'name': 'test'}
jsonData = json.dumps(data)
r = requests.post(url=url, json=jsonData)

#d = r.json()
print(r)