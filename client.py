import requests
import json

url = 'http://localhost:9115/'
#url = 'https://young-shore-84821.herokuapp.com/'
#url = 'http://flip1.engr.oregonstate.edu:8764/'
data = {'name': 'advil'}
jsonData = json.dumps(data)
print(jsonData)
r = requests.post(url=url, json=jsonData)

print(r.json())