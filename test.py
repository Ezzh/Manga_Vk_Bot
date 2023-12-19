import requests
import json

url = 'http://127.0.0.1:5000/api/add_worker'

data = {"role": 'Эдитор', "vk": 'ezzh32', "mark": '5', "note": 'bebeeb'}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())