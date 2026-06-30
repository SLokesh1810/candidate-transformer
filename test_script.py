import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

username = "SLokesh1810"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

url = f"https://api.github.com/users/{username}/repos"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
print()

print(json.dumps(response.json(), indent=4))