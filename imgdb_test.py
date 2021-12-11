
import base64
import secrets

with open("shieldingSlime.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

print(encoded_string)

# importing the requests library
import requests

# defining the api-endpoint
API_ENDPOINT = "https://api.imgbb.com/1/upload" + "?" +

# your API key here
API_KEY = secrets.IMGDB_API_KEY

# data to be sent to api
data = {'expiration': 600,
		'key': API_KEY,
        'image': "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
        }

# sending post request and saving response as response object
r = requests.post(url = API_ENDPOINT, data = data)

# extracting response text
print(r)
