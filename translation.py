import requests
import json

url = "https://microsoft-translator-text.p.rapidapi.com/translate"

async def translate(message, language, Key):
    querystring = {"to":language,"api-version":"3.0","profanityAction":"NoAction","textType":"plain"}

    payload = [{"Text": message}]
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": Key,
        #function to get the key from the .env file

        "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
    }
    return json.loads(requests.request("POST", url, json=payload, headers=headers, params=querystring).text)[0]['translations'][0]['text']