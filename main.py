import os
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.debug import debug_chat_id  # as defined below

TOKEN = os.getenv("TELEGRAM_TOKEN")
HEROKU_APP = os.getenv("HEROKU_APP_NAME")  # e.g. "gig-marketing-bot-05b0d4bfb590"
if not TOKEN or not HEROKU_APP:
    raise RuntimeError("TELEGRAM_TOKEN and HEROKU_APP_NAME must be set in Config Vars")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("chatid", debug_chat_id))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8443))
    app.run(host="0.0.0.0", port=port)
# no run_webhook here!

web_app = app

