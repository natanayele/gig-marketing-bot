from telegram import Update
from telegram.ext import ContextTypes

async def audit_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Audit mini app is under development.")