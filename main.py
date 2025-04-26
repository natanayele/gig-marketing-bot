import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from handlers.marketing import addlead_handler, listleads_handler
from handlers.manufacturing import manufacturing_handler
from handlers.civil import civil_handler
from handlers.investment import investment_handler
from handlers.funds import funds_handler
from handlers.members import members_handler
from handlers.roles import roles_handler
from handlers.admin import admin_handler
from handlers.audit import audit_handler
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define your command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to the GIG Bot!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ Help is on the way! Use /start to begin.")

# Create Application
TOKEN = os.environ.get("BOT_TOKEN")
app = ApplicationBuilder().token(TOKEN).build()

# Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("addlead", addlead_handler))
app.add_handler(CommandHandler("listleads", listleads_handler))
app.add_handler(CommandHandler("manufacturing", manufacturing_handler))
app.add_handler(CommandHandler("civil", civil_handler))
app.add_handler(CommandHandler("investment", investment_handler))
app.add_handler(CommandHandler("funds", funds_handler))
app.add_handler(CommandHandler("members", members_handler))
app.add_handler(CommandHandler("roles", roles_handler))
app.add_handler(CommandHandler("admin", admin_handler))
app.add_handler(CommandHandler("audit", audit_handler))

# Webhook for Heroku
from flask import Flask, request

web_app = Flask(__name__)

@app.on_request
async def on_request():
    await app.process_update(Update.de_json(request.get_json(force=True), app.bot))
    return "ok"

if __name__ == "__main__":
    app.run_polling()
