import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import config
import asyncio
import threading
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

bot = Bot(token=config.TELEGRAM_TOKEN)

app = Flask(__name__)
application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

from handlers.debug import debug_chat_id
application.add_handler(CommandHandler("chatid", debug_chat_id))

from handlers.marketing import forward_to_marketing
application.add_handler(CommandHandler("marketing", forward_to_marketing))

# Health check
@app.route("/", methods=["GET"])
def health_check():
    return "✅ Bot is alive"

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.json, bot)
        print(f"📦 Raw incoming update: {request.json}")

        # Delegate task to the application's task queue
        application.create_task(application.process_update(update))

    except Exception as e:
        print(f"❌ Error handling update: {e}")

    return "ok"

# 🚀 Make sure application is initialized at startup

def initialize_app():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.initialize())

    heroku_url = os.environ.get("HEROKU_URL")
    if not heroku_url:
        print("HEROKU_URL not set.")
    else:
        async def maybe_set_webhook():
            current = await bot.get_webhook_info()
            expected_url = f"{heroku_url}/webhook"

            if current.url != expected_url:
                print(f"Setting webhook to {expected_url}")
                await bot.set_webhook(expected_url)
            else:
                print("Webhook already set correctly. Skipping.")

        loop.run_until_complete(maybe_set_webhook())
    loop.close()

initialize_app()

web_app = app
