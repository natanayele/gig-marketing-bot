from telegram import Update
from telegram.ext import ContextTypes

async def members_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👥 Members mini app is under development.")