from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔧 Investment handler is under development.")

investment_handler = CommandHandler("investment", handle)
