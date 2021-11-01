import requests
import json

#url = 'http://localhost:9115/'
url = 'https://aqueous-savannah-87139.herokuapp.com/'
data = {'name': 'advil'}
jsonData = json.dumps(data)
r = requests.post(url=url, json=jsonData)

#d = r.json()
print(r)