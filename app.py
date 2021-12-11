import os
import requests
import foodSearchFunctions
from datetime import datetime as dt
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()

app = Flask(__name__)

HELP_STR1 = 'Welcome to Get the Formuoli!\n' \
           'This bot helps to get the relevant recipe and ingredient price from a food image.\n' \
           'Please follow the steps to start using the bot:\n' \
           '1. Take a picture or/and send the image to the bot.\n' \
           '2. The bot will reply with the recipe information.\n' \
           'To view this instruction message again, you can send a message containing the following' \
           'keywords: instructions, help , how to\n' \
           'Thanks for using Get the Formuoli!\n' \
           '🦴🍎🍵'

HELP_STR2 = 'To view this instruction message again, you can send a message containing the following' \
           'keywords: instructions, help , how to'

def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)


@app.route('/message', methods=['POST'])
def reply():
    sender = request.form.get('From')
    message = request.form.get('Body')
    media_url = request.form.get('MediaUrl0')
    print(f'{sender} sent {message}')

    if media_url:
        r = requests.get(media_url)
        content_type = r.headers['Content-Type']
        username = sender.split(':')[1]  # remove the whatsapp: prefix from the number
        today = str(dt.now().isoformat())
        filename_part1 = username + '_' + today
        if content_type == 'image/jpeg':
            filename = f'uploads/{username}/{filename_part1}.jpg'
        elif content_type == 'image/png':
            filename = f'uploads/{username}/{filename_part1}.png'
        else:
            filename = None
        if filename:
            if not os.path.exists(f'uploads/{username}'):
                os.mkdir(f'uploads/{username}')
            with open(filename, 'wb') as f:
                f.write(r.content)
            image_url = foodSearchFunctions.uploadImage(filename)
            results_query = foodSearchFunctions.SerpAPISearchImage(image_url)
            parsed_recipe = foodSearchFunctions.GetIngredientsAndInstructions(results_query)
            info = foodSearchFunctions.ConvertToMessages(parsed_recipe)

            return respond(info)

        else:
            return respond('This image is in an unsupported format.\n'
                           'Please submit an image in the following format: JPEG, PNG')
    else:
        return respond(HELP_STR1)
