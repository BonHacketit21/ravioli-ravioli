import requests

# api-endpoint
URL = "https://www.fairprice.com.sg/search?query=apple"

headings = {
    "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
}

# sending get request and saving the response as response object
r = requests.get(url=URL)

print(r)
print(r.text)
# extracting data in json format
# data = r.json()