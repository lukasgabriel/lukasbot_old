# lbot_functions.py

import requests

import lbot_helpers as lh

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
