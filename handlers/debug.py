from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

async def debug_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    chat_id = msg.chat.id
    logger.info(f"Chat ID: {chat_id}")
    await msg.reply_text(f"Your chat ID is: {chat_id}")
