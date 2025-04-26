from telegram import Update
from telegram.ext import ContextTypes

async def proposal_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Proposal mini app is under development.")