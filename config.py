import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
doc_id = os.getenv("DOCUMENTATION_GROUP_ID")
if doc_id is None:
    raise EnvironmentError("DOCUMENTATION_GROUP_ID is not set in the environment.")
DOCUMENTATION_GROUP_ID = int(doc_id)

doc_id = os.getenv("MARKETING_GROUP_ID")
if doc_id is None:
    raise EnvironmentError("MARKETING_GROUP_ID is not set in the environment.")
MARKETING_GROUP_ID = int(doc_id)
doc_id = os.getenv("ADMIN_USER_ID")
if doc_id is None:
    raise EnvironmentError("ADMIN_USER_ID is not set in the environment.")
ADMIN_USER_ID = int(doc_id)
