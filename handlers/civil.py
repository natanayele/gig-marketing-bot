from telegram import Update
from telegram.ext import ContextTypes

async def civil_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏗 Civil mini app is under development.")