from telegram import Update
from telegram.ext import ContextTypes

async def chatid_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"🆔 Chat ID: {chat_id}")