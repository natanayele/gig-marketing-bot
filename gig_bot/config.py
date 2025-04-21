import os
from dotenv import load_dotenv
load_dotenv()



TOKEN = os.environ.get("TELEGRAM_TOKEN")
DOCUMENTATION_GROUP_ID = int(os.environ.get("DOCUMENTATION_GROUP_ID", -1002531915136))
MARKETING_GROUP_ID     = int(os.environ.get("MARKETING_GROUP_ID", -1002523694436))


