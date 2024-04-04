import datetime

from telegram import ForceReply, Update
from telegram.ext import ContextTypes

import HelperFunctions

# command list available
command_description_tuple = [('start', 'Starts the bot'),
                             ('temp', 'Send server temperature'),
                             ('time', 'Send server date'),
                             ('shutdown', 'Shutdown the server'),
                             ('echo', 'Echo the user message'),
                             ('start_temp_inspector', 'Add temperature job to the active one'),
                             ('stop_temp_inspector', 'Remove the temperature job from the active ones'),
                             ('help', 'For a list of commands'), ]
# temperature alert value
TEMPERATURE_THRESHOLD = 60


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    text = HelperFunctions.commands_tuple_to_md(command_description_tuple)
    print(text)
    await update.message.reply_markdown(text)


async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send server time as message when the command /time is issued."""
    await update.message.reply_text(str(datetime.datetime.now()))


async def temp_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send server temperature as message when the command /temp is issued."""
    current_temp = HelperFunctions.get_server_temperature_string()
    date = datetime.datetime.now().strftime("%Y-%m-%d@%H:%M:%S")
    msg = "Server temperature at: " + date + " is " + current_temp
    await update.message.reply_text(msg)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def shutdown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shutdown the server when the command /shutdown is issued."""
    # shutdown_out = subprocess.check_output("sudo shutdown", shell=True)
    # await update.message.reply_text(str(shutdown_out))
    # context.application.shutdown()
    await update.message.reply_text(update.message.text)


async def callback_auto_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    temperature_float = HelperFunctions.get_server_temperature_float()
    job = context.job

    if temperature_float > float(TEMPERATURE_THRESHOLD):
        text = ("The temperature is above given threshold!!! \n"
                "Temperature is : ") + HelperFunctions.get_server_temperature_string()
        await context.bot.send_message(chat_id=job.chat_id, text=text)


async def command_start_temp_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add temperature job to the active one."""
    chat_id = update.effective_message.chat_id
    try:
        context.job_queue.run_repeating(callback_auto_message, 30, chat_id=chat_id, name=str(chat_id))
        text = "Correctly configurer temperature updater every 30 sec.! alert sent at " + str(
            TEMPERATURE_THRESHOLD) + HelperFunctions.CELSIUS_DEGREE
        await update.effective_message.reply_text(text)
    except (IndexError, ValueError):
        await update.effective_message.reply_text("Error while setting auto temperature updater")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def command_remove_temp_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the temperature job from the active ones."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)
