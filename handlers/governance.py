<<<<<<< HEAD
# handlers/governance.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from utils.db import get_connection

# Command: /propose title | description
def propose(update: Update, context: CallbackContext) -> None:
    if not context.args:
        update.message.reply_text("Usage: /propose title | description")
        return

    try:
        proposal_text = " ".join(context.args)
        title, description = proposal_text.split('|', 1)
        title = title.strip()
        description = description.strip()

        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO proposals (title, description) VALUES (%s, %s) RETURNING id", (title, description))
            proposal_id = cur.fetchone()["id"]
            conn.commit()
            cur.close()
            conn.close()

            # Inline voting buttons
            keyboard = [
                [
                    InlineKeyboardButton("👍 Yes", callback_data=f"vote:{proposal_id}:yes"),
                    InlineKeyboardButton("👎 No", callback_data=f"vote:{proposal_id}:no")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text(
                f"✅ Proposal #{proposal_id} Created!\n\n*Title:* {title}\n*Description:* {description}\n\n🗳 Cast your vote below:",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            update.message.reply_text("❌ Could not connect to database.")

    except ValueError:
        update.message.reply_text("⚠️ Please use `|` to separate title and description.\nExample: /propose Launch New Product | Proposal to launch a new service.", parse_mode='Markdown')


# Command: /voting proposal_id yes|no
def vote(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 2:
        update.message.reply_text("Usage: /voting proposal_id yes|no")
        return

    proposal_id, vote_value = context.args

    if vote_value.lower() not in ['yes', 'no']:
        update.message.reply_text("⚠️ Vote must be 'yes' or 'no'.")
        return

    user_id = update.effective_user.id

    conn = get_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id FROM proposals WHERE id = %s", (proposal_id,))
            if cur.fetchone() is None:
                update.message.reply_text("❌ Proposal ID not found.")
            else:
                cur.execute("INSERT INTO votes (proposal_id, user_id, vote) VALUES (%s, %s, %s)",
                            (proposal_id, user_id, vote_value.lower()))
                conn.commit()
                update.message.reply_text(
                    f"🗳 Your vote `{vote_value}` has been recorded for Proposal ID `{proposal_id}`.",
                    parse_mode='Markdown'
                )
        except Exception as e:
            print(f"❌ Voting error: {e}")
            conn.rollback()
            update.message.reply_text("❌ Failed to record your vote.")
        finally:
            cur.close()
            conn.close()
    else:
        update.message.reply_text("❌ Could not connect to database.")


# Callback handler for inline buttons
def handle_vote_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    try:
        data = query.data.split(":")
        if len(data) != 3 or data[0] != "vote":
            query.edit_message_text("❌ Invalid vote command.")
            return

        proposal_id, vote_value = data[1], data[2]
        user_id = query.from_user.id

        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT id FROM proposals WHERE id = %s", (proposal_id,))
            if cur.fetchone() is None:
                query.edit_message_text("❌ Proposal not found.")
            else:
                cur.execute("INSERT INTO votes (proposal_id, user_id, vote) VALUES (%s, %s, %s)",
                            (proposal_id, user_id, vote_value))
                conn.commit()
                query.edit_message_text(
                    f"✅ Thanks! Your vote `{vote_value}` has been recorded for Proposal #{proposal_id}.",
                    parse_mode='Markdown'
                )
            cur.close()
            conn.close()
        else:
            query.edit_message_text("❌ Could not connect to database.")

    except Exception as e:
        print(f"❌ Callback vote error: {e}")
        query.edit_message_text("❌ Failed to process your vote.")
=======
# Governance Handler

from telegram import Update
from telegram.ext import ContextTypes

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔧 Governance handler is under development.")
>>>>>>> 135d610977603ddbbe8efc390c248dd0b5a6ce2b
