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
import config

# Load environment
load_dotenv()

# Create bot & Flask app
bot = Bot(token=config.TELEGRAM_TOKEN)
app = Flask(__name__)
application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

# === Handler imports ===
from handlers.debug import debug_chat_id
from handlers.chat import chatid_handler
from handlers.marketing import marketing_router, addlead_handler, listleads_handler
from handlers.manufacturing import manufacturing_router
from handlers.civil import civil_router
from handlers.governance import governance_router, propose, vote, handle_vote_callback
from handlers.proposal import proposal_router
from handlers.vote import vote_router
from handlers.investment import investment_router
from handlers.funds import funds_router
from handlers.members import members_router
from handlers.roles import setrole_handler, roles_router
from handlers.admin import admin_router
from handlers.audit import audit_router
from handlers.dashboard import dashboard_handler

# === Register handlers ===
# Debug / utility
application.add_handler(CommandHandler("chatid", debug_chat_id))
application.add_handler(chatid_handler)

# Marketing
application.add_handler(marketing_router)
application.add_handler(addlead_handler)
application.add_handler(listleads_handler)

# Manufacturing & civil
application.add_handler(CommandHandler("manufacturing", manufacturing_router))
application.add_handler(CommandHandler("civil", civil_router))

# Governance & voting
application.add_handler(CommandHandler("propose", propose))
application.add_handler(CommandHandler("voting", vote))
application.add_handler(CallbackQueryHandler(handle_vote_callback))

# Proposals & direct votes
application.add_handler(CommandHandler("proposal", proposal_router))
application.add_handler(CommandHandler("vote", vote_router))

# Other domains
application.add_handler(CommandHandler("investment", investment_router))
application.add_handler(CommandHandler("funds", funds_router))
application.add_handler(CommandHandler("members", members_router))

# Roles & admin
application.add_handler(setrole_handler)
application.add_handler(CommandHandler("roles", roles_router))
application.add_handler(CommandHandler("admin", admin_router))
application.add_handler(CommandHandler("audit", audit_router))

# Dashboard
application.add_handler(dashboard_handler)

# === Health-check & webhook endpoint ===
@app.route("/", methods=["GET"])
def health_check():
    return "✅ Bot is alive"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.json, bot)
    application.update_queue.put_nowait(update)
    return "ok"

# === Initialize & set webhook ===
def initialize_app():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.initialize())

    heroku_url = os.getenv("HEROKU_URL")
    if heroku_url:
        async def maybe_set_webhook():
            info = await bot.get_webhook_info()
            expected = f"{heroku_url}/webhook"
            if info.url != expected:
                await bot.set_webhook(expected)
        loop.run_until_complete(maybe_set_webhook())

    loop.close()

initialize_app()

# Expose Flask app for Gunicorn
web_app = app