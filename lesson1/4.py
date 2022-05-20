import requests
import json


userid = input("Введите ваш id: ")
token = input("Введите ваш acces token: ")
response = requests.get('https://api.vk.com/method/groups.get?&access_token='+token+'&v=5.131')
j_data = response.json()

with open('groups.json', 'w') as f:
    json.dump(j_data, f)