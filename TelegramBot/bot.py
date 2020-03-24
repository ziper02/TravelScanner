import requests
import time
import platform
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from DataManager import data_manager

offical_group=0##enter the channel ID for get notifcations of bot
log_group=1##enter channel ID for getting log of bot

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


url="https://api.telegram.org/bot"+data_manager.TravelScanner_bot+"/"



hebrew_dict={
    "EasyJet":"איזי ג'ט",
    "January":"ינואר",
    "February":"פברואר",
    "March":"מרץ",
    "April":"אפריל",
    "May":"מאי",
    "June":"יוני",
    "July":"יולי",
    "August":"אוגוסט",
    "September":"ספטמבר",
    "October":"אוקטובר",
    "November":"נובמבר",
    "December":"דצמבר",
    "Amsterdam":"אמסטרדם",
    "London Stansted":"לונדון סטנסטד",
    "Berlin Schoenefeld": "ברלין שנפלד",
    "Berlin Tegal": "ברלין טגל",
    "Geneva": "ג'נבה",
    "London Gatwick": "לונדון גטוויק",
    "London Luton": "לונדון לוטון",
    "Lyon": "ליון",
    "Manchester": "מנצ'סטר",
    "Milan Malpensa": "מילאנו מלפנסה",
    "Paris Charles de Gaulle (CDG)": "פריז שארל דה גול",
}

## json send
def bot_send_message(message_text,chat_id=offical_group):

    MAX_MESSAGE_LENGTH=1000
    if len(message_text) <= MAX_MESSAGE_LENGTH:
        params = {"chat_id": chat_id, "text": message_text}
        return requests.post(url + "sendMessage", data=params)
    text = message_text
    parts = []
    while len(text) > 0:
        if len(text) > MAX_MESSAGE_LENGTH:
            part = text[:MAX_MESSAGE_LENGTH]
            first_lnbr = part.rfind('\n')
            if first_lnbr != -1:
                parts.append(part[:first_lnbr])
                text = text[first_lnbr:]
            else:
                parts.append(part)
                text = text[MAX_MESSAGE_LENGTH:]
        else:
            parts.append(text)
            break

    for part in parts:
        params = {"chat_id": chat_id, "text": part}
        requests.post(url + "sendMessage", data=params)
        time.sleep(1)



def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def start_bot():
    """Start the bot."""
    # Create the Updater
    updater = Updater(data_manager.TravelScanner_bot, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
