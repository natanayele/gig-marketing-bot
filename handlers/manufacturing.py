from telegram import Update
from telegram.ext import ContextTypes

async def manufacturing_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏭 Manufacturing mini app is under development.")