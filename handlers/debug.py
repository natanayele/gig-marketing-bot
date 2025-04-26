# handlers/debug.py
from telegram import Update
from telegram.ext import ContextTypes

async def debug_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(f"DEBUG chat_id={chat_id}")                  # this should show up in your logs
    await update.message.reply_text(f"Your chat ID is {chat_id}")
