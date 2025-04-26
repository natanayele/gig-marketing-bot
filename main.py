import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import config

# Initialize bot and app
bot = Bot(token=config.TELEGRAM_TOKEN)
app = Flask(__name__)
application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

# ---------------------- Handlers Import ----------------------

# Debug & Chat
from handlers.debug import debug_chat_id
from handlers.chat import chatid_handler

# Manufacturing Mini App
from handlers.manufacturing import manufacturing_handler

# Civil Mini App
from handlers.civil import civil_handler

# Governance Mini App
from handlers.governance import propose, vote, handle_vote_callback

# Proposal Management Mini App
from handlers.proposal import proposal_handler

# Investment Mini App
from handlers.investment import investment_handler

# Funds Management Mini App
from handlers.funds import funds_handler

# Members Management Mini App
from handlers.members import members_handler

# Roles Management Mini App
from handlers.roles import setrole_handler, roles_handler

# Admin Mini App
from handlers.admin import admin_handler

# Audit Mini App
from handlers.audit import audit_handler

# Dashboard
from handlers.dashboard import dashboard_handler, dashboard

# Marketing
from handlers.marketing import addlead_handler, listleads_handler

# ---------------------- Register Handlers ----------------------

# Debug
application.add_handler(CommandHandler("chatid", debug_chat_id))
application.add_handler(chatid_handler)

# Manufacturing
application.add_handler(CommandHandler("manufacturing", manufacturing_handler))

# Civil
application.add_handler(CommandHandler("civil", civil_handler))

# Governance
application.add_handler(CommandHandler("propose", propose))
application.add_handler(CommandHandler("voting", vote))  # renamed to /voting to avoid clash
application.add_handler(CallbackQueryHandler(handle_vote_callback))

# Proposal
application.add_handler(CommandHandler("proposal", proposal_handler))

# Investment
application.add_handler(CommandHandler("investment", investment_handler))

# Funds
application.add_handler(CommandHandler("funds", funds_handler))

# Members
application.add_handler(CommandHandler("members", members_handler))

# Roles
application.add_handler(setrole_handler)
application.add_handler(CommandHandler("roles", roles_handler))

# Admin
application.add_handler(CommandHandler("admin", admin_handler))

# Audit
application.add_handler(CommandHandler("audit", audit_handler))

# Dashboard
application.add_handler(dashboard_handler)

# Marketing
application.add_handler(addlead_handler)
application.add_handler(listleads_handler)

# ---------------------- Flask Health Check and Webhook ----------------------

@app.route("/", methods=["GET"])
def health_check():
    return "✅ Bot is alive"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.json, bot)
        print(f"📦 Raw incoming update: {request.json}")
        application.update_queue.put_nowait(update)
    except Exception as e:
        print(f"❌ Error handling update: {e}")
    return "ok"

# ---------------------- Background Task ----------------------

async def auto_dashboard_push():
    await application.initialize()
    chat_id = os.getenv("ADMIN_CHAT_ID")
    if not chat_id:
        print("❌ ADMIN_CHAT_ID not set. Skipping auto dashboard.")
        return

    while True:
        await asyncio.sleep(6 * 60 * 60)  # 6 hours
        try:
            await dashboard_push(chat_id)
        except Exception as e:
            print(f"❌ Error in auto dashboard push: {e}")

async def dashboard_push(chat_id):
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
            chat_id=chat_id,
            text=(
                f"📊 *Auto GIG Dashboard*

"
                f"🏗 Civil Proposals: {civil_count}
"
                f"🏭 Manufacturing Proposals: {manufacturing_count}
"
                f"📣 Marketing Proposals: {marketing_count}

"
                f"🗳 Total Votes Cast: {total_votes}"
            ),
            parse_mode='Markdown'
        )
    except Exception as e:
        print(f"❌ Dashboard push error: {e}")
    finally:
        cur.close()
        conn.close()

# ---------------------- Initialize Everything ----------------------

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

    # Start background tasks
    loop.create_task(auto_dashboard_push())

    loop.run_forever()

initialize_app()

web_app = app
