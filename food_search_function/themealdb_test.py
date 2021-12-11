import requests

url = "https://www.themealdb.com/api/json/v1/1/search.php?s="

response = requests.request("GET", url)

print(response.text)
