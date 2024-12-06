from telegram import Update
from telegram.ext import ContextTypes

from telegram_framework.core import BotApp


app = BotApp(__name__)

@app.command('start')
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(f"Hi {user.name}!")

@app.command('help')
async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_html(
        f"These are the available commands:\n \
        &#8226; \"<b>/start</b>\"\n \
        &#8226; \"<b>/help</b>\""
    )

@app.message()
async def msg_echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


if __name__ == "__main__":
    app.run()
