import os
import asyncio

from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
HEROKU_URL    = os.getenv("HEROKU_URL")

if not TOKEN:
    raise RuntimeError("⚠️ BOT_TOKEN not set in env")

#
#  ─── FLASK SETUP ────────────────────────────────────────────────────────────────
#
flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET"])
def health_check():
    return "✅ Bot is alive"

@flask_app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.json, bot)
    telegram_app.update_queue.put_nowait(update)
    return "ok"

#
#  ─── TELEGRAM SETUP ────────────────────────────────────────────────────────────
#
telegram_app = ApplicationBuilder().token(TOKEN).build()
bot          = Bot(token=TOKEN)

# Import your handlers (make sure each file exports the names you import here!)
from handlers.debug         import debug_chat_id
from handlers.manufacturing import manufacturing_handler
from handlers.civil         import civil_handler
from handlers.marketing     import addlead_handler, listleads_handler
# …and so on for proposal_router, investment_handler, etc.

# Register command handlers
telegram_app.add_handler(CommandHandler("chatid",       debug_chat_id))
telegram_app.add_handler(CommandHandler("manufacturing", manufacturing_handler))
telegram_app.add_handler(CommandHandler("civil",         civil_handler))
telegram_app.add_handler(CommandHandler("addlead",       addlead_handler))
telegram_app.add_handler(CommandHandler("leads",         listleads_handler))
# …and the rest of your /proposal, /investment, etc.

# Governance callbacks
from handlers.governance import propose, vote, handle_vote_callback
telegram_app.add_handler(CommandHandler("propose", propose))
telegram_app.add_handler(CommandHandler("voting", vote))
telegram_app.add_handler(CallbackQueryHandler(handle_vote_callback))

#
#  ─── AUTO-DASHBOARD PUSH ───────────────────────────────────────────────────────
#
async def dashboard_push():
    from utils.db import get_connection
    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM proposals WHERE title ILIKE '%civil%'")
        civil_count = cur.fetchone()['count']
        cur.execute("SELECT COUNT(*) FROM proposals WHERE title ILIKE '%manufacturing%'")
        manufacturing_count = cur.fetchone()['count']
        cur.execute("SELECT COUNT(*) FROM proposals WHERE title ILIKE '%marketing%'")
        marketing_count = cur.fetchone()['count']
        cur.execute("SELECT COUNT(*) FROM votes")
        total_votes = cur.fetchone()['count']

        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=(
                f"📊 *Auto GIG Dashboard*\n\n"
                f"🏗 Civil: {civil_count}\n"
                f"🏭 Manufacturing: {manufacturing_count}\n"
                f"📣 Marketing: {marketing_count}\n\n"
                f"🗳 Total Votes: {total_votes}"
            ),
            parse_mode='Markdown'
        )
    finally:
        cur.close()
        conn.close()

async def auto_dashboard_push():
    # run forever, every 6h
    await telegram_app.initialize()
    if not ADMIN_CHAT_ID:
        print("❌ ADMIN_CHAT_ID not set, skipping auto dashboard")
        return

    while True:
        await asyncio.sleep(6 * 60 * 60)
        try:
            await dashboard_push()
        except Exception as e:
            print("❌ Auto-dashboard error:", e)

def initialize_app():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(telegram_app.initialize())

    # set webhook
    if HEROKU_URL:
        async def maybe_set():
            info = await bot.get_webhook_info()
            url  = f"{HEROKU_URL}/webhook"
            if info.url != url:
                await bot.set_webhook(url)
        loop.run_until_complete(maybe_set())

    # start the background push task
    loop.create_task(auto_dashboard_push())
    loop.run_forever()

if __name__ == "__main__":
    initialize_app()

# tell Gunicorn what to serve
web_app = flask_app
