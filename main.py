import os  # ✅ <-- Add this!
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import config
import asyncio
import threading

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


def run_async_webhook():
    heroku_url = os.environ.get("HEROKU_URL")
    if not heroku_url:
        return

    async def set_hook_if_needed():
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url != f"{heroku_url}/webhook":
            await bot.set_webhook(f"{heroku_url}/webhook")

    asyncio.run(set_hook_if_needed())

threading.Thread(target=run_async_webhook).start()

web_app = app