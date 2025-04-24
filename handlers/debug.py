from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def debug_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        logger.info(f"⚙️ Full update received: {update.to_dict()}")

        if update.message is None:
            logger.warning("❌ No message in update. Cannot reply.")
            return

        chat_id = update.effective_chat.id
        logger.info(f"📥 Received /chatid in chat_id={chat_id}")
        await update.message.reply_text(f"Chat ID: `{chat_id}`", parse_mode="Markdown")

    except Exception as e:
        logger.exception("❌ Exception occurred in /chatid handler:")
