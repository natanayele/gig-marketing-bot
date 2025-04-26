from telegram import Update
from telegram.ext import ContextTypes

async def setrole(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔧 Setrole handler is under development.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔧 Roles listing handler is under development.")
