
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

# Import handlers
from handlers.debug import debug_chat_id
from handlers.marketing import addlead_handler, listleads_handler
from handlers.manufacturing import manufacturing_handler
from handlers.civil import civil_handler
from handlers.governance import propose, vote, handle_vote_callback
from handlers.proposal import proposal_handler
from handlers.investment import investment_handler
from handlers.funds import funds_handler
from handlers.members import members_handler
from handlers.roles import setrole_handler, roles_handler
from handlers.admin import admin_handler
from handlers.audit import audit_handler
from handlers.chat import chatid_handler
from handlers.dashboard import dashboard_handler, dashboard_push

# Register command handlers
application.add_handler(addlead_handler)
application.add_handler(listleads_handler)
application.add_handler(CommandHandler("chatid", debug_chat_id))
application.add_handler(CommandHandler("manufacturing", manufacturing_handler))
application.add_handler(CommandHandler("civil", civil_handler))
application.add_handler(CommandHandler("proposal", proposal_handler))
application.add_handler(CommandHandler("investment", investment_handler))
application.add_handler(CommandHandler("funds", funds_handler))
application.add_handler(CommandHandler("members", members_handler))
application.add_handler(setrole_handler)
application.add_handler(CommandHandler("roles", roles_handler))
application.add_handler(CommandHandler("admin", admin_handler))
application.add_handler(CommandHandler("audit", audit_handler))
application.add_handler(CommandHandler("chatid", chatid_handler))
application.add_handler(dashboard_handler)

# Governance specific commands
application.add_handler(CommandHandler("propose", propose))
application.add_handler(CommandHandler("voting", vote))
application.add_handler(CallbackQueryHandler(handle_vote_callback))

# Health check route
@app.route("/", methods=["GET"])
def health_check():
    return "✅ Bot is alive"

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.json, bot)
        application.update_queue.put_nowait(update)
    except Exception as e:
        print(f"❌ Error handling update: {e}")
    return "ok"

# Background task for dashboard auto-push
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

# Initialize everything
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
                print("Webhook already set correctly.")

        loop.run_until_complete(maybe_set_webhook())

    loop.create_task(auto_dashboard_push())
    loop.run_forever()

# Start the app
initialize_app()

# Gunicorn entry point
web_app = app
