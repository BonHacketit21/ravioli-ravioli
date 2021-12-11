from serpapi import GoogleSearch
import secrets
import pickle

import json



params = {
  "engine": "google_reverse_image",
  "image_url": "https://images.unsplash.com/photo-1518717758536-85ae29035b6d?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=1350&amp;q=80",
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
