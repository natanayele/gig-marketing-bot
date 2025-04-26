import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler

from handlers.debug import debug_chat_id  # your existing handler

# ─── config ───────────────────────────────────────────────────────────────────

TOKEN       = os.getenv("TELEGRAM_TOKEN")
HEROKU_APP  = os.getenv("HEROKU_APP_NAME")  # e.g. "gig-marketing-bot-05b0d4bfb590"

if not TOKEN or not HEROKU_APP:
    raise RuntimeError("TELEGRAM_TOKEN and HEROKU_APP_NAME must be set in Config Vars")

# ─── Flask vs PTB setup ─────────────────────────────────────────────────────────

bot          = Bot(token=TOKEN)
flask_app    = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

# register your commands
telegram_app.add_handler(CommandHandler("chatid", debug_chat_id))

# ─── initialize PTB app & webhook ───────────────────────────────────────────────

async def _startup():
    # initialize PTB's internal dispatcher/queue
    await telegram_app.initialize()
    # point Telegram at our /webhook route
    await bot.set_webhook(f"https://{HEROKU_APP}.herokuapp.com/webhook")

# run it right now, at import time
asyncio.get_event_loop().run_until_complete(_startup())

# ─── webhook endpoint ───────────────────────────────────────────────────────────

@flask_app.route("/webhook", methods=["POST"])
def webhook():
    upd = Update.de_json(request.json, bot)
    telegram_app.update_queue.put_nowait(upd)
    return "ok"

# ─── local dev runner ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8443"))
    flask_app.run(host="0.0.0.0", port=port)

# ─── expose to Gunicorn ──────────────────────────────────────────────────────────

web_app = flask_app
