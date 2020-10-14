import requests
import json

app_id = 7628811
vk_version = '6.14'
auth_url = f'https://oauth.vk.com/authorize?client_id=7628811&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52'

print(f'\n{auth_url}')
access_token = input('\n')

response = requests.get(f'https://api.vk.com/method/groups.get?extended=1&access_token={access_token}&v={vk_version}')
response_json = response.json()
with open('task02_response.json', 'w') as file:
    json.dump(response_json, file)

print('\n список сообществ, на которые вы подписаны')
for group in response_json['response']['items']:
    print(f"{group['name']}")

