import os
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.debug import debug_chat_id

TOKEN       = os.environ["TELEGRAM_TOKEN"]
HEROKU_APP  = os.environ["HEROKU_APP_NAME"]  # e.g. "gig-marketing-bot-05b0d4bfb590"
PORT        = int(os.environ.get("PORT", "8443"))
WEBHOOK_URL = f"https://{HEROKU_APP}.herokuapp.com/{TOKEN}"

# 1) build your Application
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("chatid", debug_chat_id))

# 2) on startup, register your webhook URL with Telegram
async def on_startup(application):
    await application.bot.set_webhook(WEBHOOK_URL)

app.post_init(on_startup)

# 3) run the built Application’s webhook server
if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_path=f"/{TOKEN}",      # path must match what you set in Telegram
        # optionally set timeouts, etc:
        # timeout=60,
    )
