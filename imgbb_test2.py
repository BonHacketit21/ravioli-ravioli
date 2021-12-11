import base64
import requests
import secrets

with open("shieldingSlime.png", "rb") as file:
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": secrets.IMGDB_API_KEY,
        "image": base64.b64encode(file.read()),
    }
    res = requests.post(url, payload)

    print(res)
    print(res.json())