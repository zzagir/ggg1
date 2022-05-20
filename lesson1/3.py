import requests
import json

username = input('Введите username: ')

response = requests.get('https://api.github.com/users/'+username+'/repos')
j_data = response.json()

repo = []
for i in j_data:
    repo.append(i['name'])
print(f'Список репозиториев пользователя {username}:\n{repo}')

with open('repositories.json', 'w') as f:
    json.dump(j_data, f)