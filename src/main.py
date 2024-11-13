import os, json, sys
# from setup import Setup

from tg import TgBot
from wa import WaBot
from ig import IgBot
from fg import FgBot

mainDir = os.path.abspath(os.path.dirname(__file__))
settings_file = os.path.join(mainDir, 'settings.json')
credentials_file = os.path.join(mainDir, 'credentials.json')
man_file = os.path.join(mainDir, 'man_file.txt')
mod_file = os.path.join(mainDir, 'modifications.json')
convo_file = os.path.join(mainDir, 'convo.json')

settings = dict(json.load(open(settings_file, 'r')))
credentials = dict(json.load(open(credentials_file, 'r')))


def main ():
    run = sys.argv[1].lower()

    if run == 'tg':
        TgBot(settings["about"], credentials["telegram"], man_file, mod_file, convo_file).main()

    elif run == 'wa':
        WaBot(credentials["whatsapp"], settings["about"], man_file).main()

    elif run == 'ig':
        IgBot(credentials["instagram"], settings["about"], man_file).main()

    elif run == 'fb':
        FgBot(credentials["facebook"], settings["about"], man_file).main()


if __name__ == "__main__":
    try:
        main()
    except IndexError:
        print("\033[1;91m[-] IshaStartupError:\033[0m \033[1mPlease specify any one of the following: tg, wa, ig, fb\033[0m")
