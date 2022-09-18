# two important objects for building a functional Telegram bot:
# telegram.ext.Updater: receives messages from Telegram (messenger app) and sends them to Dispatcher
# telegram.ext.Dispatcher: sends the message to a handle function that will process the message and
#                          generate a reply

import telegram
from api_IGNORE import API_key
from telegram.ext import Updater, MessageHandler, Filters

bot = telegram.Bot(token=API_key)

# function that implements the message handler, which echoes the user's mssg back to them
# update: an incoming message (text, image, etc)
# context: contains attributes that hold data from the same chat and user (the convo's context)
# this is our message handler's callback function
def echo(update, context):
    update.message.reply_text(update.message.text)

# creating an Updater instance
updater = Updater(API_key, use_context=True)

# registering a handler to handle input text messages
updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

# start polling updates from the messenger app (happens infinitely until update occurs)
updater.start_polling()
updater.idle()  # blocks the script until a message is received



# to stop infinitely polling, enter CTRL + C into the terminal 