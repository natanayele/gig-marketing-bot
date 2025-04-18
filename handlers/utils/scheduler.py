from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz

async def send_daily_report(context):
    await context.bot.send_message(chat_id='@yourgroup', text="Daily Marketing Update: [details here]")

def setup_scheduler(app):
    scheduler = AsyncIOScheduler(timezone=pytz.utc)
    scheduler.add_job(send_daily_report, 'cron', hour=12, minute=0, args=[app])
    scheduler.start()
