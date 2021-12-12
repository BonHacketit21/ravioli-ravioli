import base64
import requests
from serpapi import GoogleSearch
import secrets


def uploadImage(img_path):

    with open(img_path, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": secrets.IMGBB_API_KEY,
            "expiration": 120,
            "image": base64.b64encode(file.read()),
        }
        res = requests.post(url, payload)

        if res.status_code == 200:
            json = res.json()
            print(json['data']['url'])
            return json['data']['url']

        else:
            return None

def SerpAPISearchImage(img_url):
    params = {
        "engine": "google_reverse_image",
        "image_url": img_url,
        "api_key": secrets.SERPAPI_API_KEY,
        "hl": "en",
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    #print(results)
    #print(results["search_information"])
    #print(results["search_information"]['query_displayed'])
    return results["search_information"]['query_displayed']


def GetIngredientsAndInstructions(searchFood):
    url = "https://www.themealdb.com/api/json/v1/1/search.php?s=" + searchFood

    res = requests.request("GET", url)
    json = res.json()
    print(json)

    title = json['meals'][0]['strMeal']
    instructions_strings = json['meals'][0]['strInstructions'].strip().split('.')
    instructions = []
    ingredients = []
    ingredients_amounts = []

    #print(instructions_strings)

    for line in instructions_strings:
        instructions.append(line.strip() + ".")

    for i in range(1, 21):
        ingredient = "strIngredient" + str(i)
        measure = "strMeasure" + str(i)

        if json['meals'][0][ingredient] != None and json['meals'][0][ingredient] != "":
            ingredients.append(json['meals'][0][ingredient])
            ingredients_amounts.append(json['meals'][0][measure] + " " + json['meals'][0][ingredient])
        else:
            break
    youtube = json['meals'][0]['strYoutube']
    return [title, instructions, ingredients, ingredients_amounts, youtube]


def ConvertToMessages(parsed_recipe):
    messages = ''

    heading = "Dish: " + parsed_recipe[0] + "\n"

    ingredients_message = heading + "Ingredients:\n"

    ingredients_list = parsed_recipe[3]
    for ingredient in ingredients_list:
        # ingredients_message += ingredient + " ~ " + getPriceForItem(ingredient) + "\n"
        ingredients_message += ingredient + "\n"

    messages += ingredients_message + "\n"

    instructions = parsed_recipe[1]
    new_message = "Instructions:\n"
    total_length = len(new_message)


    for line in instructions:
        if (total_length + len(line) + 1) < 700:
            new_message += line + "\n"
            total_length += len(line) + 1
        else:
            messages += new_message
            total_length = len(line) + 1
            new_message = line + "\n"

    messages += new_message

    messages += "\n" + parsed_recipe[4]

    return messages

def getPriceForItem(item_name):
    params = {
        "q": item_name,
        "tbm": "shop",
        "location": "Singapore",
        "hl": "en",
        "gl": "us",
        "api_key": secrets.SERPAPI_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    price = results['shopping_results'][0]['price']

    return price

## Example usage
image_url = uploadImage("images/carrot cake.jpg")
results_query = SerpAPISearchImage(image_url)
print(results_query)
parsed_recipe = GetIngredientsAndInstructions(results_query)
messages = ConvertToMessages(parsed_recipe)

#print(parsed_recipe)
#print('\n')

print(messages)
