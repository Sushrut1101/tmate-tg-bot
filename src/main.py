from telegram.ext import ApplicationBuilder, CommandHandler
from src.modules import commands

app = ApplicationBuilder().token("").build()

app.add_handler(CommandHandler("new", commands.handle_new))
app.add_handler(CommandHandler("list", commands.handle_list))
app.add_handler(CommandHandler("kill", commands.handle_kill))
app.add_handler(CommandHandler("show", commands.handle_show))

if __name__ == "__main__":
    app.run_polling()
