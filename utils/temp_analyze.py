import requests
import json

urls = [
    'https://open.spotify.com/playlist/0YizqBuL8K7fiXN8DMZSb3',
    'https://open.spotify.com/playlist/2mT6LpOU4ipJ0BkoCigAiw',
    'https://open.spotify.com/playlist/5KWf8H2pM0tlVd7niMtqeU',
    'https://open.spotify.com/playlist/6q0rnAIIxokcRlu6vRJPNX'
]

# Assuming your Flask app is running on http://localhost:5000
response = requests.post('http://localhost:5000/api/analyze-batch', json={'playlist_urls': urls})

print(json.dumps(response.json(), indent=2))