from pathlib import Path
import atexit
import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from src.modules import commands, session_manager
from src.modules.authorize import load_authorized
from src.modules.logger import ts

def main():
    load_dotenv(dotenv_path=Path.cwd() / ".env")
    print(f"[{ts()}] [INFO] Environment variables loaded...")

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable not set")

    load_authorized()

    print(f"[{ts()}] [INFO] Bot started...")

    atexit.register(session_manager.cleanup_all_sessions)

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start",   commands.handle_start))
    app.add_handler(CommandHandler("help",    commands.handle_help))
    app.add_handler(CommandHandler("new",     commands.handle_new))
    app.add_handler(CommandHandler("list",    commands.handle_list))
    app.add_handler(CommandHandler("kill",    commands.handle_kill))
    app.add_handler(CommandHandler("show",    commands.handle_show))
    app.add_handler(CommandHandler("killall", commands.handle_killall))

    app.run_polling()

if __name__ == "__main__":
    main()
