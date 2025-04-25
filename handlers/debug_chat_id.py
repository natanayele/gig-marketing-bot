# Debug handler to get chat ID

async def debug_chat_id(update, context):
    await update.message.reply_text(f"🆔 Chat ID: {update.effective_chat.id}")
