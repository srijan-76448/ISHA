from telegram import *
from telegram.ext import *
import os, json
from datetime import datetime
from head import Brain


mainDir = os.path.abspath(os.path.dirname(__file__))
settings_file = os.path.join(mainDir, 'settings.json')
credentials_file = os.path.join(mainDir, 'credentials.json')
manual_file = os.path.join(mainDir, 'manual.txt')
modifications_file = os.path.join(mainDir, 'modifications.json')
convo_file = os.path.join(mainDir, 'convo.json')

settings = dict(json.load(open(settings_file, 'r')))
credentials = dict(dict(json.load(open(credentials_file, 'r')))["telegram"])
modifications = list(json.load(open(modifications_file, 'r')))


RUN: bool = None
convo = {}
settings["verbose"] = False


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resp = f"Hello {update.message.from_user.first_name}! I am ISHA, your Interactive Smart Home Assistant.\n\nI am still under development."
    RUN = True
    update_convo(str(update.message.chat.id), update.message.chat.full_name, update.message.text, resp, update.message.chat.type)
    await update.message.reply_text(text=resp)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global manual
    manual = open(manual_file, 'r').read()

    if RUN:
        update_convo(str(update.message.chat.id), update.message.chat.full_name, update.message.text, manual, update.message.chat.type)
        await update.message.reply_text(text=manual)


async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if RUN:
        update_convo(str(update.message.chat.id), update.message.chat.full_name, update.message.text, json.dumps(settings["about"]), update.message.chat.type)
        await update.message.reply_text(text=json.dumps(settings["about"], indent=4))


def handle_response(txt: str) -> str:
    return Brain(txt.lower())


async def handle_mod(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resp = "Thanks for your suggestion! Your suggestion has been saved."
    mod = update.message.text.replace("/mod ", "")
    suggested_by = update.message.from_user.first_name

    modification = {
        "suggested_by": suggested_by,
        "modification": mod
    }

    modifications.append(modification)

    if RUN:
        update_convo(str(update.message.chat.id), update.message.chat.full_name, update.message.text, resp, update.message.chat.type)
        await update.message.reply_text(text=resp)
        json.dump(modifications, open(modifications_file, 'w'), indent=4)


async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_type: str = update.message.chat.type
    txt: str = update.message.text
    resp = ""

    if msg_type == "group":
        if credentials["user-name"] in txt:
            txt: str = txt.replace(credentials["user-name"], "")
            resp: str = handle_response(txt)

        else:
            return

    else:
        resp = handle_response(txt)

    if RUN:
        update_convo(str(update.message.chat.id), update.message.chat.full_name, txt, resp, msg_type)
        await update.message.reply_text(text=resp)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"\033[1;31m[-] TelegramBotError:\033[0m \033[1mUpdate \033[1;33m{update}\033[0m caused error \033[1m{context.error}\033[0m]")


def update_convo(userid: str, username: str, input_text: str, response: str, convo_type: str):
    convo = dict(json.load(open(convo_file, "r")))

    if userid not in convo.keys():
        convo[userid] = {"username": username, "private": [], "group": []}

    convo[userid][convo_type].append({
        "input": input_text, 
        "response": response,
        "timestamp": f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} IST"
    })

    json.dump(convo, open(convo_file, "w"), indent=4)
    printf(json.dumps(convo, indent=4))


def printf(txt: str):
    if settings["verbose"]:
        print(txt)


def main():
    print("\033[1;32m[+]\033[0m \033[1mStarting Bot...\033[0m")
    app = Application.builder().token(credentials["api-key"]).build()

    # Commands
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about_cmd))

    app.add_handler(CommandHandler("mod", handle_mod))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_msg))

    # Errors
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)


if __name__ == "__main__":
    main()