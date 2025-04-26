from telegram import Update
from telegram.ext import ContextTypes

async def funds_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💵 Funds section under development.")
