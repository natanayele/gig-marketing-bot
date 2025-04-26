from telegram import Update
from telegram.ext import ContextTypes

async def admin_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑 Admin mini app is under development.")