import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

def get_env_var(key: str, fallback=None, required: bool = True):
    val = os.getenv(key, fallback)
    if required and val is None:
        raise EnvironmentError(f"Missing required environment variable: {key}")
    return val

DOCUMENTATION_GROUP_ID = int(get_env_var("DOCUMENTATION_GROUP_ID"))
MARKETING_GROUP_ID = int(get_env_var("MARKETING_GROUP_ID"))
TELEGRAM_TOKEN = get_env_var("TELEGRAM_TOKEN", fallback="test-token", required=False)
