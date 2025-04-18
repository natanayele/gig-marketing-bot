from telegram import Update
from telegram.ext import ContextTypes

async def team_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This week’s team meetings:\n- Monday: Project Sync\n- Wednesday: Marketing Meeting\n- Friday: Review & Wrap-up")
