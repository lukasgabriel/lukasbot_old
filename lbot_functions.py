# lbot_functions.py

import requests
import googletrans

import lbot_helpers as lh
import lbot_data as ld

import os
from dotenv import load_dotenv

load_dotenv()


# returns the urban dictionary definition for the user-specified search term - powered by UrbanScraper (http://urbanscraper.herokuapp.com/).
# I know this is ugly code, but I couldn't think of an easier way to check different cases of the search term.
def get_urban_definition(term):
    response = requests.get(url=f"http://urbanscraper.herokuapp.com/define/{term}")
    if response.status_code == 200:
        term = response.json()["term"]
        definition = response.json()["definition"]
        url = response.json()["url"]
        example = response.json()["example"]
        return term, definition, url, example
    elif response.status_code == 404:
        term = term.lower()
        response = requests.get(url=f"http://urbanscraper.herokuapp.com/define/{term}")
        if response.status_code == 200:
            term = response.json()["term"]
            definition = response.json()["definition"]
            url = response.json()["url"]
            example = response.json()["example"]
            return term, definition, url, example
        elif response.status_code == 404:
            term = term.upper()
            response = requests.get(
                url=f"http://urbanscraper.herokuapp.com/define/{term}"
            )
            if response.status_code == 200:
                term = response.json()["term"]
                definition = response.json()["definition"]
                url = response.json()["url"]
                example = response.json()["example"]
                return term, definition, url, example
            elif response.status_code == 404:
                term = term.title()
                response = requests.get(
                    url=f"http://urbanscraper.herokuapp.com/define/{term}"
                )
                if response.status_code == 200:
                    term = response.json()["term"]
                    definition = response.json()["definition"]
                    url = response.json()["url"]
                    example = response.json()["example"]
                    return term, definition, url, example
                elif response.status_code == 404:
                    return False
    else:
        raise lh.APIError(
            code=response.status_code,
            url=f"http://urbanscraper.herokuapp.com/define/{term}",
            headers=response.headers,
            msg=response.reason,
            text=response.text,
        )


# translate text using the google translate API via googletrans
def translate(text="Please specify a text string to translate.", src="auto", dest="en"):
    translator = googletrans.Translator()
    translated = translator.translate(text, dest=dest, src=src)
    return translated


def tl_from_discord(raw_args):
    text = raw_args[0].strip()
    if len(text) == 0:
        msgresponse = "Please specify a text string to translate."
        return msgresponse
    try:
        dest = raw_args[1].strip()
    except:
        dest = "en"
    try:
        src = raw_args[2].strip()
    except:
        src = "auto"

    if (
        dest != "auto"
        and dest.lower() not in googletrans.LANGUAGES
        and dest.lower() not in googletrans.LANGCODES
    ):
        msgresponse = f"Language {dest} not found. View https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages for all languages and language codes."
        return msgresponse
    if (
        src != "auto"
        and src.lower() not in googletrans.LANGUAGES
        and src.lower() not in googletrans.LANGCODES
    ):
        msgresponse = f"Language {src} not found. View https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages for all languages and language codes."
        return msgresponse

    try:
        translated = translate(text, src, dest)
        msgresponse = f">>> Translation from {googletrans.LANGUAGES[translated.src].title()} to {googletrans.LANGUAGES[translated.dest].title()}: \n \n {translated.origin} :arrow_right: {translated.text}"
        return msgresponse
    except ValueError:
        msgresponse = ">>> Invalid command format. Use '>help tl' for more info."
        return msgresponse
    except Exception as e:
        msgresponse = ">>> An error occured. @bot_dad"
        raise e

    return msgresponse


def clap_case(text):
    return text.strip().upper().replace(" ", " :clap: ") + " :clap: "

def start_on_client(application):
    try:
        NGROK_URL = os.getenv("NGROK_URL")
    except:
        print("Error: Missing ngrok URL in environment variables.")
        raise EnvironmentError

    url = NGROK_URL + application
    response = requests.get(url=url)
    return response.status_code
