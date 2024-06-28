import requests

url = "http://127.0.0.1:8000/get_title"
payload = {"title": "This is a test sentence.", "threshold": 0.7}
response = requests.post(url, json=payload)
print(response.json())