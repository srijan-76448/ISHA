from telegram import *
from telegram.ext import *
from datetime import datetime
from head import Brain
import os, json


Tutorial = "https://youtu.be/vZtm1wuA2yc?si=0ym9z4uYtT8dyOmB"


class TgBot:
    def __init__(self, settings: dict, credentials: dict, manual_file: str, modifications_file: str, convo_file: str):
        self.settings = settings
        self.credentials = credentials
        self.manual_file = manual_file
        self.modifications_file = modifications_file
        self.convo_file = convo_file

        self.modifications = list(json.load(open(modifications_file, 'r')))
        self.convo = {}

    async def start_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        resp = f"Hello {update.message.from_user.first_name}! I am ISHA, your Interactive Smart Home Assistant.\n\nI am still under development."
        self.update_convo(str(update.message.chat.id), update.message.chat.full_name, update.message.text, resp, update.message.chat.type)
        await update.message.reply_text(text=resp)

    async def help_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.manual = open(self.manual_file, 'r').read()

        self.update_convo(str(update.message.chat.id), update.message.chat.full_name, update.message.text, self.manual, update.message.chat.type)
        await update.message.reply_text(text=self.manual)

    async def about_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.update_convo(str(update.message.chat.id), update.message.chat.full_name, update.message.text, json.dumps(self.settings["about"]), update.message.chat.type)
        await update.message.reply_text(
            text=json.dumps(self.settings["about"], indent=4)
        )

    async def handle_mod(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        resp = "Thanks for your suggestion! Your suggestion has been saved."

        self.update_mod(update.message.text.replace("/mod ", ""), update.message.from_user.first_name)
        self.update_convo(str(update.message.chat.id), update.message.chat.full_name, update.message.text, resp, update.message.chat.type)
        await update.message.reply_text(text=resp)

    async def handle_msg(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg_type: str = update.message.chat.type
        txt: str = update.message.text
        resp = ""

        if msg_type == "group":
            if self.credentials["user-name"] in txt:
                txt: str = txt.replace(self.credentials["user-name"], "")
                resp: str = self.handle_response(txt)

            else:
                return

        else:
            resp = self.handle_response(txt)

        self.update_convo(str(update.message.chat.id), update.message.chat.full_name, txt, resp, msg_type)
        await update.message.reply_text(text=resp)

    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.printe("IshaTelegramBotUpdateError", f"Update \033[1;33m{update}\033[0m caused error \033[1m{context.error}")

    def printe(self, error_type: str, error_txt: str):
        print(f"\033[1;31m[-] {error_type}:\033[0m \033[1m{error_txt}\033[0m")

    def prints(self, success_type: str, success_txt: str):
        print(f"\033[1;32m[+] {success_type}:\033[0m \033[1m{success_txt}\033[0m")

    def printw(self, txt: str):
        print(f"\033[1;33m[*]\033[0m \033[1m{txt}\033[0m")

    def printf(self, txt: str, verbose: bool = None):
        vb = self.settings["verbose"] if verbose is None else verbose
        if vb: print(txt)

    def update_convo(self, userid: str, username: str, input_text: str, response: str, convo_type: str):
        self.convo = dict(json.load(open(self.convo_file, "r")))

        if userid not in self.convo.keys():
            self.convo[userid] = {"username": username, "private": [], "group": []}

        self.convo[userid][convo_type].append({
            "input": input_text, 
            "response": response,
            "timestamp": f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} IST"
        })

        json.dump(self.convo, open(self.convo_file, "w"), indent=4)
        self.printf(json.dumps(self.convo, indent=4))

    def update_mod(self, modification: str, suggested_by: str):
        mods = list(json.load(open(self.modifications_file, 'r')))
        mods.append({"suggested_by": suggested_by, "modification": modification})
        json.dump(mods, open(self.modifications_file, 'w'), indent=4)

    def handle_response(self, txt: str) -> str:
        txt: str = txt.lower()
        ret: str = Brain(txt)
        return ret

    def main(self):
        app = Application.builder().token(self.credentials["api-key"]).build()
        self.prints("IshaTelegramBotStartup", "Starting Bot...")

        # Commands
        app.add_handler(CommandHandler("start", self.start_cmd))
        app.add_handler(CommandHandler("help", self.help_cmd))
        app.add_handler(CommandHandler("about", self.about_cmd))

        app.add_handler(CommandHandler("mod", self.handle_mod))

        # Messages
        app.add_handler(MessageHandler(filters.TEXT, self.handle_msg))

        # Errors
        app.add_error_handler(self.error)

        print("Polling...")
        app.run_polling(poll_interval=3)
