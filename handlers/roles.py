from telegram import Update
from telegram.ext import ContextTypes

async def roles_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎭 Roles section under development.")
