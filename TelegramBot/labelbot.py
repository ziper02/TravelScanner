import json
import logging
import os
import calendar
from datetime import datetime

from data_manager import data_manager
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler

from Entity.Flight import Flight
from Utilities import general

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


file_loaded=False
flights=[]
global json_file_flights
FIRST, SECOND = range(2)

def start(update, context):
    global file_loaded
    global flights
    global json_file_flights
    if update.message== None:
        input=update.callback_query.message
    else:
        input=update.message
    if not file_loaded:
        flights,json_file_flights=load_next_label_file()
        if flights is None:
            input.reply_text("Finished to label all the data.")
            return
        file_loaded= True
    for flight in flights:
        if flight.label == -1:
            depart_date_temp = datetime.strptime(flight.depart_date, '%Y-%m-%d')
            return_date_temp = datetime.strptime(flight.return_date, '%Y-%m-%d')
            day_name_depart=calendar.day_name[depart_date_temp.weekday()]
            day_name_return = calendar.day_name[return_date_temp.weekday()]
            input.reply_text("The destination is " + flight.destination.name +
                                    "\nThe depature date is " + flight.depart_date +
                                      "\nThe return date is " + flight.return_date +
                                        "\n"+day_name_depart+" until "+day_name_return+
                                      "\nThe price is " + str(flight.price))
            keyboard = [[InlineKeyboardButton("רע", callback_data='1'),
                         InlineKeyboardButton("בינוני", callback_data='2'),
                         InlineKeyboardButton("טוב", callback_data='3')],
                        [InlineKeyboardButton("עצור", callback_data='4')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            input.reply_text('Please choose:', reply_markup=reply_markup)
            return FIRST
    with open(os.path.dirname(__file__)+"/../" + json_file_flights, 'w',encoding='utf-8') as f:
        json.dump(flights, f, ensure_ascii=False, default=general.obj_dict, indent=4)
    file_loaded=False
    input.reply_text('Press /start again')
    return




def load_next_label_file():
    with open(os.path.dirname(__file__) + '/../Data/Flights/json_files.json') as f:
        json_files = json.load(f)
    for json_file in json_files:
        flights_data = []
        with open(os.path.dirname(__file__)+"/../" + json_file) as f:
            data = json.load(f)
        for temp in data:
            flights_data.append(Flight(**temp))
        for flight in flights_data:
            if flight.label==(-1):
                return flights_data,json_file
    return None,None

def button(update, context):
    global file_loaded
    global flights
    global  START
    global json_file_flights
    query = update.callback_query
    answer_from_user=int(query.data)
    if answer_from_user== 4:
        finish_label()
        update.callback_query.message.reply_text('Press /start again')
        return
    else:
        for flight in flights:
            if flight.label == -1:
                if answer_from_user == 1:
                    flight.label = 1
                    break
                elif answer_from_user == 2:
                    flight.label = 2
                    break
                elif answer_from_user == 3:
                    flight.label = 3
                    break
        keyboard = [
            [InlineKeyboardButton(u"המשך", callback_data='6')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text('Please press Next:', reply_markup=reply_markup)
        return SECOND
    return


def finish_label():
    global flights
    global json_file_flights
    global file_loaded
    with open(os.path.dirname(__file__)+"/../" + json_file_flights, 'w', encoding='utf-8') as f:
        json.dump(flights, f, ensure_ascii=False, default=general.obj_dict, indent=4)
    file_loaded=False


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(data_manager.Label_bot, use_context=True)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [CallbackQueryHandler(button)],
            SECOND: [CallbackQueryHandler(start)]
        },
        fallbacks=[CommandHandler('start', start)]
    )
    updater.dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()