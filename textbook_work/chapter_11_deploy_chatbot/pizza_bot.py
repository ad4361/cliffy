import spacy
import telegram
from api_IGNORE import API_key
from telegram.ext import Updater, MessageHandler, Filters

bot = telegram.Bot(token=API_key)

# this code is taken from chapter_8_intent/syn_prdefined_list.py
def extract_intent(doc):
    # extract transitive verb/dobj
    for token in doc:
        if token.dep_ == 'dobj':
            dobj = token.text.lower()
            verb = token.head.text.lower()

    # create a list of tuples for possible verb synonyms
    verbList = [('order', 'want', 'give', 'make'), ('show', 'find')]
    # find the tuple containing the transitive verb that was extracted above
    verbSynonyms = [item for item in verbList if verb in item]


    # create a list of tuples for possible direct object synonyms
    dobjList = [('pizza', 'pie', 'dish', 'pizzas'), ('cola', 'soda')]
    # find the tuple containing the dobj that was extracted above
    dobjSynonyms = [item for item in dobjList if dobj in item]


    # replace the trans verb and dobj with synonyms supported by the application (the syns at top of list)
    # to compose the string that expressed the intent
    if len(verbSynonyms) == 0 or len(dobjSynonyms) == 0:
        intent = 'unrecognized'
    else:
        intent = verbSynonyms[0][0] + dobjSynonyms[0][0].capitalize()
    
    return intent



# callback function
def utterance(update, context):
    msg = update.message.text
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(msg)
    for token in doc:
        if token.dep_ == 'dobj':    # dobj present in user input
            intent = extract_intent(doc)
            if intent == 'orderPizza':
                update.message.reply_text('We need some more information to place your order.')
            elif intent == 'showPizza': 
                update.message.reply_text('Would you like to see our menu?')
            elif intent == 'orderCola':
                update.message.reply_text('We need some more information to place your drink order.')
            elif intent == 'showCola': 
                update.message.reply_text('Would you like to see our menu?')
            else:
                update.message.reply_text('Your intent is not recognized.')
            return
    
    # no dobj found
    update.message.reply_text('Please rephrase your request. Be as specific as possible!')




# create updater and register message handler
updater = Updater(API_key, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.text, utterance))

# wait for responses
updater.start_polling()
updater.idle()

