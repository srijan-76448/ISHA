# import nltk
import os, json


mainDir = os.path.abspath(os.path.dirname(__file__))
settings = dict(dict(json.load(open(os.path.join(mainDir, 'settings.json'), 'r')))["about"])


def Brain(inpt: str, inpt_img = None) -> str:
    inpt: str = inpt.lower()
    ret = f"you said: {inpt}"

    if "hi" in inpt:
        ret = "Hello!"

    return ret.capitalize()
