import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler
from dotenv import load_dotenv

load_dotenv()  # make sure your TELEGRAM_TOKEN is in your .env / Config Vars

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN is not set!")

# build your bot
application = ApplicationBuilder().token(TOKEN).build()

# register only the debug handler
from handlers.debug import debug_chat_id
application.add_handler(CommandHandler("chatid", debug_chat_id))

# flask app for webhook
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), Bot(token=TOKEN))
    application.update_queue.put_nowait(update)
    return "ok"

# expose Flask app to gunicorn
web_app = app
