from telegram import Update
from telegram.ext import ContextTypes
from . import session_manager

async def handle_new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sid, ssh_url = session_manager.create_session()
    await update.message.reply_text(f"✅ Created: {sid}\n🔗 SSH: `{ssh_url}`", parse_mode="Markdown")

async def handle_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sessions = session_manager.list_sessions()
    if sessions:
        msg = "\n".join([f"🔸 {sid}" for sid in sessions])
    else:
        msg = "🚫 No active sessions."
    await update.message.reply_text(msg)

async def handle_kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("⚠️ Usage: /kill <session_id>")
        return

    if session_manager.kill_session(args[0]):
        await update.message.reply_text(f"💀 Session {args[0]} killed.")
    else:
        await update.message.reply_text("❌ Session not found.")

async def handle_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("⚠️ Usage: /show <session_id>")
        return

    ssh_url = session_manager.get_ssh_url(args[0])
    if ssh_url:
        await update.message.reply_text(f"🔗 SSH URL for {args[0]}:\n`{ssh_url}`", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Session not found.")
