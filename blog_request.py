import requests 

api = 'http://127.0.0.1:8000/api/v1/2'

response = requests.get(api)

print(response.json())