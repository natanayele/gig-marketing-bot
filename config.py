import os
from dotenv import load_dotenv
# handlers/debug.py
from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

async def debug_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    chat_id = msg.chat.id
    logger.info(f"Chat ID: {chat_id}")
    await msg.reply_text(f"Your chat ID is: {chat_id}")


# Load environment variables from a .env file if present
load_dotenv()

def get_env_var(key: str, fallback=None, required: bool = True):
    val = os.getenv(key, fallback)
    if required and val is None:
        raise EnvironmentError(f"Missing required environment variable: {key}")
    return val

DOCUMENTATION_GROUP_ID = int(get_env_var("DOCUMENTATION_GROUP_ID"))
MARKETING_GROUP_ID = int(get_env_var("MARKETING_GROUP_ID"))
TELEGRAM_TOKEN = get_env_var("TELEGRAM_TOKEN", fallback="test-token", required=False)
