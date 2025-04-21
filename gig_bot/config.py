import os
from dotenv import load_dotenv

load_dotenv()

DOCUMENTATION_GROUP_ID = int(os.environ.get("DOCUMENTATION_GROUP_ID", "123456"))
MARKETING_GROUP_ID = int(os.environ.get("MARKETING_GROUP_ID", "654321"))
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "test-token")
