import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.debug import debug_chat_id  # your existing handler

# -- logging (optional, but helpful) --
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# -- config vars --
TOKEN = os.getenv("TELEGRAM_TOKEN")
HEROKU_APP = os.getenv("HEROKU_APP_NAME")  # e.g. "gig-marketing-bot-05b0d4bfb590"
if not TOKEN or not HEROKU_APP:
    raise RuntimeError("TELEGRAM_TOKEN and HEROKU_APP_NAME must be set in Config Vars")

# -- build your Application --
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("chatid", debug_chat_id))

def main():
    port = int(os.environ.get("PORT", 8443))
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path="webhook",
        webhook_url=f"https://{HEROKU_APP}.herokuapp.com/webhook",
    )

if __name__ == "__main__":
    main()
