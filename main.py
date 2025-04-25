# Trigger rebuild

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

<<<<<<< HEAD
# Import handlers
from handlers.debug import debug_chat_id
from handlers.marketing import marketing_router
=======
from handlers.debug import debug_chat_id
from handlers.marketing import marketing_router

from handlers.manufacturing import manufacturing_router
from handlers.civil import civil_router
# from handlers.governance import governance_router
from handlers.vote import vote_router
from handlers.proposal import proposal_router
from handlers.investment import investment_router
from handlers.funds import funds_router
from handlers.members import members_router
from handlers.roles import roles_router
from handlers.admin import admin_router
from handlers.audit import audit_router
from handlers.chat import chatid_handler


application.add_handler(CommandHandler("chatid", debug_chat_id))
application.add_handler(CommandHandler("marketing", marketing_router))
application.add_handler(CommandHandler("manufacturing", manufacturing_router))
application.add_handler(CommandHandler("civil", civil_router))
application.add_handler(CommandHandler("governance", governance_router))
application.add_handler(CommandHandler("vote", vote_router))
application.add_handler(CommandHandler("proposal", proposal_router))
application.add_handler(CommandHandler("investment", investment_router))
application.add_handler(CommandHandler("funds", funds_router))
application.add_handler(CommandHandler("members", members_router))
application.add_handler(CommandHandler("roles", roles_router))
application.add_handler(CommandHandler("admin", admin_router))
application.add_handler(CommandHandler("audit", audit_router))
application.add_handler(CommandHandler("chatid", chatid_handler))


from handlers.civil import civil_router
>>>>>>> 135d610977603ddbbe8efc390c248dd0b5a6ce2b
from handlers.manufacturing import manufacturing_router
from handlers.civil import civil_router
from handlers.governance import propose, vote, handle_vote_callback  # Added callback
from handlers.vote import vote_router
from handlers.proposal import proposal_router
from handlers.investment import investment_router
from handlers.funds import funds_router
from handlers.members import members_router
from handlers.roles import setrole_handler  # Added setrole handler
from handlers.roles import roles_router  # keep if exists
from handlers.admin import admin_router
from handlers.audit import audit_router
from handlers.chat import chatid_handler
from handlers.dashboard import dashboard_handler  # Added dashboard handler
from handlers.marketing import addlead_handler, listleads_handler

application.add_handler(addlead_handler)
application.add_handler(listleads_handler)


# Add command handlers
application.add_handler(CommandHandler("chatid", debug_chat_id))
application.add_handler(CommandHandler("marketing", marketing_router))
application.add_handler(CommandHandler("manufacturing", manufacturing_router))
application.add_handler(CommandHandler("civil", civil_router))
application.add_handler(CommandHandler("vote", vote_router))
application.add_handler(CommandHandler("proposal", proposal_router))
application.add_handler(CommandHandler("investment", investment_router))
application.add_handler(CommandHandler("funds", funds_router))
application.add_handler(CommandHandler("members", members_router))
application.add_handler(setrole_handler)  # Register setrole command
application.add_handler(CommandHandler("roles", roles_router))
application.add_handler(CommandHandler("admin", admin_router))
application.add_handler(CommandHandler("audit", audit_router))
application.add_handler(CommandHandler("chatid", chatid_handler))
application.add_handler(dashboard_handler)  # Register dashboard command

# Governance specific commands: /propose and /vote
application.add_handler(CommandHandler("propose", propose))
application.add_handler(CommandHandler("voting", vote))  # Avoid conflict: renamed from /vote
application.add_handler(CallbackQueryHandler(handle_vote_callback))  # Inline voting callback


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
        application.update_queue.put_nowait(update)
    except Exception as e:
        print(f"❌ Error handling update: {e}")
    return "ok"

# Initialize application and webhook
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

# Call the initializer
initialize_app()

web_app = app
