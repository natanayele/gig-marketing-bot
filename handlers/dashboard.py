from telegram import Update
from telegram.ext import ContextTypes

async def dashboard_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Dashboard mini app is under development.")

async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Dashboard details are coming soon!")