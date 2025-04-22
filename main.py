import os  # ✅ <-- Add this!
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import config
import asyncio

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
async def webhook():
    update = Update.de_json(request.json, bot)
    await application.process_update(update)
    return "ok"

@app.before_first_request
def init_webhook():
    heroku_url = os.environ.get("HEROKU_URL")
    if heroku_url:
        # schedule webhook to be set after the app starts
        asyncio.get_event_loop().create_task(bot.set_webhook(f"{heroku_url}/webhook"))

web_app = app
