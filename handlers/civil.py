from telegram import Update
from telegram.ext import ContextTypes

async def civil_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏗️ Civil Engineering section under development.")
