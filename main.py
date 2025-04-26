import os
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN      = os.environ["TELEGRAM_TOKEN"]
HEROKU_APP = os.environ["HEROKU_APP_NAME"]
PORT       = int(os.environ.get("PORT", "8443"))

application = (
    ApplicationBuilder()
    .token(TOKEN)
    .webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=f"https://{HEROKU_APP}.herokuapp.com/webhook",
    )
    .build()
)

from handlers.debug import debug_chat_id
application.add_handler(CommandHandler("chatid", debug_chat_id))

if __name__ == "__main__":
    application.run_webhook()
