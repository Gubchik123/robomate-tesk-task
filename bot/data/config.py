import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = [
    int(admin_chat_id) for admin_chat_id in str(os.getenv("ADMINS")).split(",")
]

BASE_DIR = Path(__file__).parent.parent

JOB_SITES = [
    os.path.basename(dir[0]).replace("_", ".")
    for dir in os.walk(BASE_DIR / "utils" / "resumes")
    if not os.path.basename(dir[0]).endswith("__")
][1:]
