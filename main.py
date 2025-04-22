import os  # ✅ <-- Add this!
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import config

bot = Bot(token=config.TELEGRAM_TOKEN)

app = Flask(__name__)
application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

# Register your handlers
from handlers.marketing import forward_to_marketing
application.add_handler(CommandHandler("marketing", forward_to_marketing))

# Health check
@app.route("/", methods=["GET"])
def health_check():
    return "✅ Bot is alive"

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.json, bot)
    application.create_task(application.process_update(update))
    return "ok"


# Set webhook once when the server starts
def set_webhook():
    heroku_url = os.environ.get("HEROKU_URL")  # e.g. https://yourapp.herokuapp.com
    if heroku_url:
        bot.set_webhook(f"{heroku_url}/webhook")

# Call it right after Flask app setup
set_webhook()


web_app = app
