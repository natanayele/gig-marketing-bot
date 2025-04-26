from telegram import Update
from telegram.ext import ContextTypes

async def propose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔧 Propose handler is under development.")

async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔧 Vote handler is under development.")

async def handle_vote_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer("Vote recorded!")
