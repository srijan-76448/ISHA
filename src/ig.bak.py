import os, json
from instabot import *


mainDir = os.path.abspath(os.path.dirname(__file__))
settings = dict(json.load(open(os.path.join(mainDir, 'settings.json'), 'r')))
credentials = dict(dict(json.load(open(os.path.join(mainDir, 'credentials.json'), 'r')))["instagram"])



bot = Bot()
logged_in = bot.login(
    username=credentials["user-name"],
    password=credentials["password"]
)


def test():
    print(f"\033[1;92m[+] LoginSuccess:\033[0m \033[1mLogged in successfully as {credentials['user-name']}\033[0m")


if logged_in:
    test()

else:
    print(f"\033[1;91m[-] LoginError:\033[0m \033[1mFailed to login into {credentials['user-name']}\033[0m")