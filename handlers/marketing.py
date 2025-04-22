from telegram import Update
from telegram.ext import ContextTypes
import logging
from gig_bot import config


logger = logging.getLogger(__name__)

async def forward_to_marketing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        msg = update.message
        chat_id = msg.chat.id
        user = msg.from_user

        logger.debug(f"[DEBUG] Incoming chat_id={chat_id}, expected={config.DOCUMENTATION_GROUP_ID}")

        if chat_id != config.DOCUMENTATION_GROUP_ID:
            logger.warning(f"Unauthorized access to /marketing from chat_id={chat_id}")
            await msg.reply_text("Sorry, this command is only available in the documentation group.")
            return

        # Extract the message after /marketing
        text = msg.text.partition(" ")[2]
        if not text.strip():
            await msg.reply_text("Usage: /marketing <your message>")
            return

        formatted = f"[Marketing Bot]\nFrom {user.first_name}: {text}"
        await context.bot.send_message(chat_id=config.MARKETING_GROUP_ID, text=formatted)
        await msg.reply_text("✅ Message forwarded to Marketing group.")
        logger.info(f"Forwarded message from {chat_id} to {config.MARKETING_GROUP_ID}")

    except Exception as e:
        logger.exception("❌ Error in forward_to_marketing")
        await update.message.reply_text("⚠️ Something went wrong while forwarding your message.")
