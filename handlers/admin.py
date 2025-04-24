# Admin Handler

from telegram import Update
from telegram.ext import ContextTypes

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔧 Admin handler is under development.")
