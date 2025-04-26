from telegram import Update
from telegram.ext import ContextTypes

async def investment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 Investment section under development.")
