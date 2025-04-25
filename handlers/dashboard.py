# handlers/dashboard.py

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from utils.db import get_connection

# 📊 Dashboard Command
async def dashboard(update: Update, context: CallbackContext):
    text = await generate_dashboard_text()
    await update.message.reply_text(text, parse_mode='Markdown')

# 📊 Dashboard Auto-Push (background task support)
async def dashboard_push(bot, chat_id):
    text = await generate_dashboard_text()
    await bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')

# 🧠 Helper Function to Fetch Dashboard Data
async def generate_dashboard_text():
    conn = get_connection()
    if not conn:
        return "❌ Database connection error."

    try:
        cur = conn.cursor()

        # Count proposals per business unit
        cur.execute("SELECT COUNT(*) FROM proposals WHERE title ILIKE '%civil%'")
        civil_count = cur.fetchone()['count']

        cur.execute("SELECT COUNT(*) FROM proposals WHERE title ILIKE '%manufacturing%'")
        manufacturing_count = cur.fetchone()['count']

        cur.execute("SELECT COUNT(*) FROM proposals WHERE title ILIKE '%marketing%'")
        marketing_count = cur.fetchone()['count']

        # Total votes
        cur.execute("SELECT COUNT(*) FROM votes")
        total_votes = cur.fetchone()['count']

        # Leads (Marketing CRM)
        cur.execute("SELECT COUNT(*) FROM leads")
        lead_count = cur.fetchone()['count']

        return (
            f"📊 *GIG Dashboard*\n\n"
            f"🏗 Civil Proposals: {civil_count}\n"
            f"🏭 Manufacturing Proposals: {manufacturing_count}\n"
            f"📣 Marketing Proposals: {marketing_count}\n\n"
            f"🗳 Total Votes: {total_votes}\n"
            f"📋 Marketing Leads: {lead_count}\n"
        )

    except Exception as e:
        print(f"❌ Dashboard query error: {e}")
        return "❌ Error generating dashboard."
    finally:
        cur.close()
        conn.close()

# 📎 Export the dashboard handler
dashboard_handler = CommandHandler("dashboard", dashboard)
