import requests

url = "http://127.0.0.1:8000/get_tags_api"
payload = {"title": "This is a test sentence. about python api", "threshold": 1.3}
response = requests.post(url, json=payload)
print(response.json())