from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from utils.db import get_connection
import re

# 📥 Add Lead Command
async def add_lead(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /addlead <Name> <Email>")
        return

    name = context.args[0]
    email = context.args[1]

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

        text = "📋 *Leads List:*

"
        for row in rows:
            text += f"- {row['name']} ({row['email']})\n"

        await update.message.reply_text(text, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text("❌ Error fetching leads.")
        print(f"DB error: {e}")
    finally:
        cur.close()
        conn.close()

addlead_handler = CommandHandler("addlead", add_lead)
listleads_handler = CommandHandler("leads", list_leads)
