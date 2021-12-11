import requests

url = "https://tasty.p.rapidapi.com/recipes/auto-complete"

querystring = {"prefix":"chicken soup"}

headers = {
    'x-rapidapi-host': "tasty.p.rapidapi.com",
    'x-rapidapi-key': "5fa50b5560msh48dd449c272f6f8p1e8bb9jsn521335125eee"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)