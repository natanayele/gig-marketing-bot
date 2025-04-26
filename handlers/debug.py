from telegram import Update
from telegram.ext import ContextTypes

async def debug_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"🆔 Chat ID: {chat_id}")