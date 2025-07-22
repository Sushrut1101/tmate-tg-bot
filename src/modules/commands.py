from telegram import Update
from telegram.ext import ContextTypes

from . import session_manager

async def handle_new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Spawning tmate session…")
    sid, urls = session_manager.create_session()

    lines = [f"✅ Session `{sid}` created:"]
    if urls.get("ssh_rw"):
        lines.append(f"🔐 RW SSH: `{urls['ssh_rw']}`")
    if urls.get("ssh_ro"):
        lines.append(f"🔑 RO SSH: `{urls['ssh_ro']}`")
    if urls.get("web_rw"):
        lines.append(f"🌐 RW Web: {urls['web_rw']}")
    if urls.get("web_ro"):
        lines.append(f"🌐 RO Web: {urls['web_ro']}")

    if len(lines) == 1:
        lines.append("🚫 No connection URLs available.")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

async def handle_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    active = session_manager.list_sessions()
    if not active:
        await update.message.reply_text("🚫 No active sessions.")
    else:
        msg = "\n".join(f"🔸 {sid}" for sid in active)
        await update.message.reply_text(msg)

async def handle_kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        return await update.message.reply_text("⚠️ Usage: /kill <session_id>")

    sid = args[0]
    ok  = session_manager.kill_session(sid)
    text = f"💀 Killed `{sid}`." if ok else "❌ Session not found."
    await update.message.reply_text(text)

async def handle_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        return await update.message.reply_text("⚠️ Usage: /show <session_id>")

    sid = args[0]
    urls = session_manager.get_urls(sid)
    if not urls:
        return await update.message.reply_text("❌ Session not found.")

    lines = []
    if urls.get("ssh_rw"):
        lines.append(f"🔐 RW SSH: `{urls['ssh_rw']}`")
    if urls.get("ssh_ro"):
        lines.append(f"🔑 RO SSH: `{urls['ssh_ro']}`")
    if urls.get("web_rw"):
        lines.append(f"🌐 RW Web: {urls['web_rw']}")
    if urls.get("web_ro"):
        lines.append(f"🌐 RO Web: {urls['web_ro']}")

    if not lines:
        lines.append("🚫 No connection URLs available.")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
