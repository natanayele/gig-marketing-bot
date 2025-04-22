from telegram import Update
from telegram.ext import ContextTypes
import logging
import config

logger = logging.getLogger(__name__)

async def forward_to_marketing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        msg = update.message
        if not msg:
            logger.warning("No message found in update")
            return

        user = msg.from_user
        chat_id = msg.chat.id

        logger.debug(f"[DEBUG] Incoming chat_id={chat_id}, expected={config.DOCUMENTATION_GROUP_ID}")

        if chat_id != config.DOCUMENTATION_GROUP_ID:
            logger.warning(f"Unauthorized access to /marketing from chat_id={chat_id}")
            await msg.reply_text("⚠️ Sorry, this command is only available in the documentation group.")
            return

        # Extract the message after the command
        text = msg.text.partition(" ")[2]
        if not text.strip():
            await msg.reply_text("ℹ️ Usage: /marketing <your message>")
            return

        formatted = f"📢 *Marketing Bot*\n👤 From: {user.first_name} (@{user.username or 'unknown'})\n\n{text}"
        await context.bot.send_message(chat_id=config.MARKETING_GROUP_ID, text=formatted, parse_mode="Markdown")
        await msg.reply_text("✅ Your message was forwarded to the Marketing team.")
        logger.info(f"✅ Forwarded message from chat_id={chat_id} to marketing group.")

    except Exception as e:
        logger.exception("❌ Exception in forward_to_marketing")
        if update.effective_chat:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Something went wrong while forwarding your message.")
