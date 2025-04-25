# handlers/marketing.py

# Marketing Handler

from telegram import Update
from telegram.ext import ContextTypes

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔧 Marketing handler is under development.")

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from utils.db import get_connection
import re

# 📥 Add Lead Command
async def add_lead(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /addlead <Name> <Email>")
        return

    name = context.args[0]
    email = context.args[1]

    # Basic email validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        await update.message.reply_text("⚠️ Invalid email format.")
        return

    conn = get_connection()
    if not conn:
        await update.message.reply_text("❌ Database connection error.")
        return

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO leads (name, email) VALUES (%s, %s)",
            (name, email)
        )
        conn.commit()
        await update.message.reply_text(f"✅ Lead added: {name} ({email})")
    except Exception as e:
        await update.message.reply_text("❌ Error adding lead.")
        print(f"DB error: {e}")
    finally:
        cur.close()
        conn.close()

# 📋 List Leads Command
async def list_leads(update: Update, context: CallbackContext):
    conn = get_connection()
    if not conn:
        await update.message.reply_text("❌ Database connection error.")
        return

    try:
        cur = conn.cursor()
        cur.execute("SELECT name, email FROM leads ORDER BY created_at DESC LIMIT 20")
        rows = cur.fetchall()

        if not rows:
            await update.message.reply_text("No leads found.")
            return

        text = "📋 *Leads List:*\n\n"
        for row in rows:
            text += f"- {row['name']} ({row['email']})\n"

        await update.message.reply_text(text, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text("❌ Error fetching leads.")
        print(f"DB error: {e}")
    finally:
        cur.close()
        conn.close()

# 📎 Export handlers
addlead_handler = CommandHandler("addlead", add_lead)
listleads_handler = CommandHandler("leads", list_leads)
    if action == "post":
        if not params:
            await message.reply_text("⚠️ Please provide a message to post.")
        else:
            text_to_post = ' '.join(params)
            # Here you could broadcast this to other channels or store
            await message.reply_text(f"📣 Marketing post received:\n{text_to_post}")
    else:
        await message.reply_text(f"❓ Unknown marketing action: {action}")


