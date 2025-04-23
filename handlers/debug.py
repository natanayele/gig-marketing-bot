import logging
logger = logging.getLogger(__name__)

async def debug_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        chat_id = update.effective_chat.id
        logger.info(f"📥 Received /chatid in chat_id={chat_id}")
        await update.message.reply_text(f"Chat ID: `{chat_id}`", parse_mode="Markdown")
    except Exception as e:
        logger.exception("❌ Error in /chatid")
