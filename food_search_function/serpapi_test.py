from serpapi import GoogleSearch
import secrets
import pickle

import json

params = {
  "engine": "google_reverse_image",
  "image_url": "https://tmbidigitalassetsazure.blob.core.windows.net/rms3-prod/attachments/37/1200x1200/exps41527_CS143613B11_11_8b.jpg",
  "api_key": secrets.SERPAPI_TOKEN
}

search = GoogleSearch(params)
results = search.get_dict()

with open('convert.txt', 'w') as convert_file:
  convert_file.write(json.dumps(results))

with open('data.json', 'wb') as fp:
  pickle.dump(results, fp)

with open('data.json', 'rb') as fp:
  data = pickle.load(fp)
print(data)
print(type(data))

# inline_images = results['inline_images']
