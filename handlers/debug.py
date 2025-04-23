# handlers/debug.py
from telegram import Update
from telegram.ext import ContextTypes

async def debug_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Chat ID: `{chat_id}`", parse_mode="Markdown")
