import requests, json

#get list of rooms
url = "https://api.daily.co/v1/rooms"
headers = {'authorization': 'Bearer 05535c097075d1938caf827de2217e51a56cf2309a9c738443b8df7a47e2054b'}
response = requests.request("GET", url, headers=headers)
print(response.text)
data = response.json()

#delete all rooms in list
for room in data['data']:
	url = "https://api.daily.co/v1/rooms/" + room['name']
	response = requests.request("DELETE", url, headers=headers)
	print(response.text)