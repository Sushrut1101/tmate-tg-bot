from telegram import Update
from telegram.ext import ContextTypes

from . import session_manager, authorize, logger

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(user_id, "/start")
    await update.message.reply_text(
        "👋 Hello! I’m your tmate session manager bot.\n\n"
        "Use /help to see available commands."
    )

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(user_id, "/help")
    await update.message.reply_text(
        "📖 Available commands:\n"
        "/new — Create a new tmate session\n"
        "/list — Show all active sessions\n"
        "/show <id> — Show session URLs\n"
        "/kill <id> — Kill a session\n"
        "/killall — Kill all sessions\n"
        "/help — Show this help message\n\n"
        "🚫 Access is restricted to authorized users."
    )

async def handle_new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not authorize.is_authorized(update):
        logger.deny(user_id, "/new")
        return await authorize.reject(update)

    sid, urls = session_manager.create_session()
    msg = (
        f"✅ Session `{sid}` created:\n\n"
        f"🔐 RW SSH: `{urls.get('ssh_rw', 'N/A')}`\n"
        f"🔑 RO SSH: `{urls.get('ssh_ro', 'N/A')}`\n"
        f"🌐 RW Web: {urls.get('web_rw', 'N/A')}\n"
        f"🌐 RO Web: {urls.get('web_ro', 'N/A')}"
    )
    logger.info(user_id, "/new", msg)
    await update.message.reply_text(msg, parse_mode="Markdown")

async def handle_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not authorize.is_authorized(update):
        logger.deny(user_id, "/list")
        return await authorize.reject(update)

    sessions = session_manager.list_sessions()
    msg = "\n".join(f"🔸 {sid}" for sid in sessions) if sessions else "🚫 No active sessions."
    logger.info(user_id, "/list", msg)
    await update.message.reply_text(msg)

async def handle_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not authorize.is_authorized(update):
        logger.deny(user_id, "/show")
        return await authorize.reject(update)

    args = context.args
    if not args:
        msg = "⚠️ Usage: /show <session_id>"
        logger.info(user_id, "/show", msg)
        return await update.message.reply_text(msg)

    sid = args[0]
    urls = session_manager.get_urls(sid)
    if not urls:
        msg = "❌ Session not found."
        logger.info(user_id, f"/show {sid}", msg)
        return await update.message.reply_text(msg)

    msg = (
        f"🔐 RW SSH: {urls.get('ssh_rw', 'N/A')}\n"
        f"🔑 RO SSH: {urls.get('ssh_ro', 'N/A')}\n"
        f"🌐 RW Web: {urls.get('web_rw', 'N/A')}\n"
        f"🌐 RO Web: {urls.get('web_ro', 'N/A')}"
    )
    logger.info(user_id, f"/show {sid}", msg)
    await update.message.reply_text(msg)

async def handle_kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not authorize.is_authorized(update):
        logger.deny(user_id, "/kill")
        return await authorize.reject(update)

    args = context.args
    if not args:
        msg = "⚠️ Usage: /kill <session_id>"
        logger.info(user_id, "/kill", msg)
        return await update.message.reply_text(msg)

    sid = args[0]
    ok = session_manager.kill_session(sid)
    msg = f"💀 Killed `{sid}`." if ok else "❌ Session not found."
    logger.info(user_id, f"/kill {sid}", msg)
    await update.message.reply_text(msg)

async def handle_killall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not authorize.is_authorized(update):
        logger.deny(user_id, "/killall")
        return await authorize.reject(update)

    count = len(session_manager.list_sessions())
    session_manager.cleanup_all_sessions()

    msg = f"💥 Killed {count} session(s)." if count else "🚫 No active sessions."
    logger.info(user_id, "/killall", msg)
    await update.message.reply_text(msg)
