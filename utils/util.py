import os
import re
import json
import random
from os.path import join, dirname

from dotenv import load_dotenv

def get_env(env_key, filepath):
    """ Get environment variables """
    
    dotenv_path = join(dirname(filepath), '.env')
    load_dotenv(dotenv_path)

    try: 
        return os.getenv(env_key)
    except Exception as e:
        return e

def is_keyword_mentioned(text):
    with open('config/triggers.json', 'r') as triggers:
        keywords = json.load(triggers)
    for keyword in keywords:
        if re.search(keyword, text, re.IGNORECASE):
            return True

    return False

def get_random_quote(_type=None):
    quotes_file = 'config/quotes.json'
    if _type == 'jaskier':
        quotes_file = 'config/responsesToJaskier.json'
    with open(quotes_file, 'r') as quotes:
        geralt_quotes = json.load(quotes)

    return random.choice(geralt_quotes)

def get_username(author):
    if not author:
        name = '[deleted]'
    else:
        name = author.name
    
    return name