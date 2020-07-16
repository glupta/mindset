import requests

url = "https://api.daily.co/v1/meeting-tokens"

payload = "{\"properties\":{\"room_name\":\"room1\"}}"
headers = {
    'content-type': "application/json",
    'authorization': "Bearer 05535c097075d1938caf827de2217e51a56cf2309a9c738443b8df7a47e2054b"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)

url = "https://api.daily.co/v1/meeting-tokens/" + response.json()['token']
print(url)

headers = {'authorization': 'Bearer 05535c097075d1938caf827de2217e51a56cf2309a9c738443b8df7a47e2054b'}

response = requests.request("GET", url, headers=headers)

print(response.text)