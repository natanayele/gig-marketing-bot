from telegram import Update
from telegram.ext import ContextTypes
from utils.permissions import is_from_allowed_group, is_admin
from config import MARKETING_GROUP_ID

async def marketing_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if not is_from_allowed_group(update, MARKETING_GROUP_ID) and not is_admin(update):
        await update.message.reply_text("🚫 Access denied. Marketing commands are restricted.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("🧭 Please provide a marketing task. Example: /marketing promote")
        return

    task = args[0].lower()
    if task == "promote":
        await update.message.reply_text("📣 Marketing team notified to promote content.")
    else:
        await update.message.reply_text(f"🤖 Unknown marketing task: {task}")
