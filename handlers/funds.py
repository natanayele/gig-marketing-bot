from telegram import Update
from telegram.ext import ContextTypes

async def funds_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 Funds mini app is under development.")