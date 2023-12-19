import requests
import json, uuid
import random
import string

url1 = 'http://192.168.0.18:5000/api/add_worker'
url2 = 'http://192.168.0.18:5000/api/add_request'
for i in range(5):
    data2 = {"captain": str(uuid.uuid1()), "project": "".join(random.choice(string.ascii_letters) for _ in range(10)), "worker": random.choice(["Translator", "Editor", "Gangsta", "Заведующий кафедры", "Ректор"]), "bet":str(random.randint(0, 100000)) + "$", "condition": str(random.randint(0, 30)) + "d", "other": "".join(random.choice(string.ascii_letters) for _ in range(10))}
    data1 = {"role": random.choice(["Translator", "Editor", "Gangsta", "Заведующий кафедры", "Ректор"]), "vk": str(uuid.uuid1()), "mark":random.randint(0, 10), "note": "".join(random.choice(string.ascii_letters) for _ in range(10))}
    response1 = requests.post(url1, json=data1)
    response2 = requests.post(url2, json=data2)
    print(response1.json())
    print(response2.json())