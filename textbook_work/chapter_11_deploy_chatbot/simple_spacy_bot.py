
import spacy
import telegram
from api_IGNORE import API_key
from telegram.ext import Updater, MessageHandler, Filters

bot = telegram.Bot(token=API_key)

# callback function for text user input
# processes a user's utterance and determines if it contains a direct object
def utterance(update, context):
    msg = update.message.text   # user input
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(msg)

    for token in doc:
        if token.dep_ == 'dobj':
            update.message.reply_text('Your request has a direct object, and we are processing it...')
            return  # dobj found, break from loop
    update.message.reply_text('Your request lacks a direct object. Please rephrase your request.')


# creating an Updater instance
updater = Updater(API_key, use_context=True)

# registering a handler to handle input text messages
updater.dispatcher.add_handler(MessageHandler(Filters.text, utterance))

# start polling updates from the messenger app (happens infinitely until update occurs)
updater.start_polling()
updater.idle() # blocks the script until a message is received

