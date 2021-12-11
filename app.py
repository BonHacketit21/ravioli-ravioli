import os
import requests
import foodSearchFunctions
from datetime import datetime as dt
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()

app = Flask(__name__)

HELP_STR1 = 'Welcome to *Get the Formuoli*!\n' \
            'This bot helps to get the relevant recipe and ingredient price from a food image.\n' \
            '*Please follow the steps to start using the bot:*\n' \
            'To use an _image_ to get the recipe:\n' \
            '1. Take a picture or/and send the image to the bot.\n' \
            '2. The bot will reply with the recipe information.\n' \
            'To use _keywords_ to get the recipe:\n' \
            "1. Enter the command: _!formuoli_ followed by ```keywords```\n" \
            "2. The bot will reply with the recipe information\n" \
            'To *view this instruction message* again, you can send a message containing the following ' \
            'keywords: _instructions_, _help_ , _how to_\n' \
            'Thanks for using Get the Formuoli!\n' \
            '🦴🍎🍵'

HELP_STR2 = 'Invalid command.\n' \
            'To view this instruction message again, you can send a message containing the following ' \
            'keywords:\ninstructions, help , how to'


def get_message_img(fn):
    image_url = foodSearchFunctions.uploadImage(fn)
    results_query = foodSearchFunctions.SerpAPISearchImage(image_url)
    parsed_recipe = foodSearchFunctions.GetIngredientsAndInstructions(results_query)
    return foodSearchFunctions.ConvertToMessages(parsed_recipe)


def get_message_txt(term):
    parsed_recipe = foodSearchFunctions.GetIngredientsAndInstructions(term)
    return foodSearchFunctions.ConvertToMessages(parsed_recipe)


def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)


@app.route('/message', methods=['POST'])
def reply():
    sender = request.form.get('From')
    message = request.form.get('Body').lower()
    media_url = request.form.get('MediaUrl0')
    print(f'{sender} sent {message}')

    if '!formuoli' in message:
        print('here')
        keywords = message.replace('!formuoli ', '')

        if keywords == '':
            return respond('No search term given. Please try again with keywords.')

        info = get_message_txt(keywords)
        return respond(info)

    elif 'help' in message or 'instruction' in message or 'how to' in message:
        print('help')
        return respond(HELP_STR1)

    elif media_url:
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
            info = get_message_img(filename)

            return respond(info)

        else:
            return respond('This image is in an unsupported format.\n'
                           'Please submit an image in the following format: JPEG, PNG')
    else:
        return respond(HELP_STR2)
