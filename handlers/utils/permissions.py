from telegram import Update
from config import ADMIN_USER_ID, DOCUMENTATION_GROUP_ID, MARKETING_GROUP_ID

def is_from_allowed_group(update: Update, allowed_group_id: int) -> bool:
    chat_id = update.effective_chat.id
    return chat_id == allowed_group_id

def is_admin(update: Update) -> bool:
    return update.effective_user.id == ADMIN_USER_ID
