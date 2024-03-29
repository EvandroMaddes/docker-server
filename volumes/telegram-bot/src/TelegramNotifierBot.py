## pyhton instllaer + env creation
## https://stackoverflow.com/questions/75602063/pip-install-r-requirements-txt-is-failing-this-environment-is-externally-mana

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

import Commands

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(Commands.command_description_tuple)


def main() -> None:
    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    """Start the bot."""

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token).post_init(post_init).build()
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", Commands.start))
    application.add_handler(CommandHandler("help", Commands.help_command))
    application.add_handler(CommandHandler("time", Commands.time_command))
    application.add_handler(CommandHandler("temp", Commands.temp_command))
    application.add_handler(CommandHandler("shutdown", Commands.shutdown_command))
    application.add_handler(CommandHandler("start_temp_inspector", Commands.command_start_temp_job))
    application.add_handler(CommandHandler("stop_temp_inspector", Commands.command_remove_temp_job))
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, Commands.echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
