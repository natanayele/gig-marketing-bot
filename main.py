import os
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.debug import debug_chat_id

# pull in your env vars
TOKEN      = os.environ["TELEGRAM_TOKEN"]
HEROKU_APP = os.environ["HEROKU_APP_NAME"]   # e.g. "gig-marketing-bot-05b0d4bfb590"
PORT       = int(os.environ.get("PORT", "8443"))
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL  = f"https://{HEROKU_APP}.herokuapp.com{WEBHOOK_PATH}"

# this coroutine will run right after the app starts up
async def on_startup(app):
    # tell Telegram where to POST updates
    await app.bot.set_webhook(WEBHOOK_URL)

# build your Application *with* the startup hook
app = (
    ApplicationBuilder()
    .token(TOKEN)
    .post_init(on_startup)   # <-- register it on the builder
    .build()
)

# register your handlers
app.add_handler(CommandHandler("chatid", debug_chat_id))

if __name__ == "__main__":
    # serve your webhook endpoint
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_path=WEBHOOK_PATH,
    )
