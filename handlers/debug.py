from telegram import Update
from telegram.ext import ContextTypes

async def debug_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Chat ID: {update.effective_chat.id}")
