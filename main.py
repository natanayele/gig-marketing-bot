from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import config

# Forward specific messages from Documentation Group to Marketing Group
async def forward_to_marketing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.chat.id == config.DOCUMENTATION_GROUP_ID:
        if message.text and message.text.startswith("/marketing"):
            # Clean up the command prefix
            clean_message = message.text.replace("/marketing", "").strip()

            # Forward message to marketing group
            await context.bot.send_message(
                chat_id=config.MARKETING_GROUP_ID,
                text=f"📢 From Documentation Team:\n\n{clean_message}"
            )

            # Confirmation in Documentation group
            await message.reply_text("✅ Message forwarded to Marketing Team.")

# Command to directly communicate to marketing from private chat with bot
async def direct_marketing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        msg = ' '.join(context.args)
        await context.bot.send_message(
            chat_id=config.MARKETING_GROUP_ID,
            text=f"📢 Direct Message from {update.effective_user.first_name}:\n\n{msg}"
        )
        await update.message.reply_text("✅ Your message has been sent to the Marketing Team.")
    else:
        await update.message.reply_text("Please include a message after /marketing command.")

def main():
    app = ApplicationBuilder().token(config.TOKEN).build()

    # Handler for forwarding messages with /marketing prefix
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), forward_to_marketing))
    
    # Handler for direct communication from private chats
    app.add_handler(CommandHandler("marketing", direct_marketing))

    print("🤖 Bot is active and monitoring...")
    app.run_polling()

if __name__ == "__main__":
    main()
