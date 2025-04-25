
# Civil Handler

from telegram import Update
from telegram.ext import ContextTypes

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔧 Civil handler is under development.")

from telegram import Update
from telegram.ext import ContextTypes

async def civil_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    message_text = update.message.text
    args = context.args

    if not args:
        await update.message.reply_text("🧭 Please enter a civil task. Example: /civil design")
        return

    task = args[0].lower()

    if task == "design":
        await update.message.reply_text("📐 Civil design team will review the task.")
    else:
        await update.message.reply_text(f"🏗️ Unknown civil task: {task}")

