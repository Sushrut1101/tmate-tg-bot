import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from src.modules import commands

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
token = os.getenv("BOT_TOKEN")

if not token:
    raise ValueError("BOT_TOKEN environment variable not set")

app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("new", commands.handle_new))
app.add_handler(CommandHandler("list", commands.handle_list))
app.add_handler(CommandHandler("kill", commands.handle_kill))
app.add_handler(CommandHandler("show", commands.handle_show))

if __name__ == "__main__":
    app.run_polling()
