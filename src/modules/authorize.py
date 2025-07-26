from telegram import Update
import os

AUTHORIZED_USERS = set()

def load_authorized():
    raw = os.getenv("AUTHORIZED_USERS", "")
    if not raw:
        raise ValueError("AUTHORIZED_USERS environment variable not set")
    global AUTHORIZED_USERS
    AUTHORIZED_USERS = set(s.strip() for s in raw.split(",") if s.strip())

def is_authorized(update: Update) -> bool:
    return str(update.effective_user.id) in AUTHORIZED_USERS

async def reject(update: Update):
    await update.message.reply_text("⛔ You are not authorized to use this bot!")
