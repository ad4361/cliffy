# definite improvements can be made to this bot, but I'm gonna move on now :)

import logging
import sys
import spacy
from api_IGNORE import API_key
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler

# for obtaining generic debug info:
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


# helper function used during by 'ORDERING' state's callback function
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


# converts the contents of user_data from a dictionary to a string
# user_data will contain info such as the type and number of pizzas the user wants, and will be 
#           updated throughout the script
def details_to_str(user_data):
    details = list()
    for key, value in user_data.items():
        details.append('{} - {}'.format(key, value))
    return "\n".join(details).join(['\n', '\n'])



# entry point's callback function, will execute as soon as conversation starts 
def start(update, context):
    update.message.reply_text('Hi! This is a pizza ordering app. What would you like to order?')
    return 'ORDERING'



# 'ORDERING' state's callback function
def intent_extraction(update, context):
    msg = update.message.text
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(msg)
    for token in doc:
        if token.dep_ == 'dobj':    
            # runs if dobj present in user input
            intent = extract_intent(doc)
            
            if intent == 'orderPizza':
                context.user_data['product'] = 'pizza'
                update.message.reply_text('We need some more information to place your order. What type of pizza do you want?')
                return 'ADD_INFO'

            elif intent == 'showPizza': 
                update.message.reply_text('Would you like to see our menu?')
                return 'SHOW_MENU'
            
            else:
                update.message.reply_text('Your intent is not recognized. Please rephrase your request.')
            return 'ORDERING'
    
    # no dobj found
    update.message.reply_text('Please rephrase your request. Be as specific as possible!')
    return 'ORDERING'



# callback function for 'SHOW_MENU' state
def show_menu(update, context):
    msg = update.message.text
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(msg)

    # ideally, you would take pizza types from a database
    pizza_types = ['Cheese', 'Veggie', 'Pepperoni','Hawaiian', 'BBQ Chicken', 'Greek']

    affirmative = ['yes', 'yeah', 'ok', 'okay']
    negative = ['no']

    for token in doc:
        if token.text.lower() in affirmative:
            update.message.reply_text('Here is our menu of pizza options: \n' '{}'.format("\n".join(pizza_types)))
            return 'ORDERING'
        elif token.text.lower() in negative:
            update.message.reply_text('What would you like to order?')
            return 'ORDERING'
        else:
            update.message.reply_text('Your intent is not recognized. Please rephrase your request.')
            return 'SHOW_MENU'



# 'ADD_INFO' state's callback function
def add_info(update, context):
    msg = update.message.text
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(msg)

    pizza_types_lower = ['cheese', 'veggie', 'pepperoni', 'hawaiian', 'bbq chicken', 'greek']

    for token in doc:
        if token.dep_ == 'dobj':
            dobj = token
            # search for modifiers to dobj 
            for child in dobj.lefts:
                if child.dep_ == 'amod' or child.dep_ == 'compound':
                    
                    # modifier found
                    modifier = child.text

                    if modifier.lower() in pizza_types_lower:
                        context.user_data['type'] = modifier
                        user_data = context.user_data
                        
                        update.message.reply_text('Your order has been placed.' '{}' 'Have a nice day!'.format(details_to_str(user_data)))
                        return ConversationHandler.END 

                    elif modifier not in pizza_types_lower:
                        update.message.reply_text('This pizza type is not available. Please try specifying another type of pizza.')
                        return 'ADD_INFO'

    
    # no dobj with modifiers found
    update.message.reply_text('Cannot extract necessary info. Please try again.')
    return 'ADD_INFO'



def cancel(update, context):
    update.message.reply_text('Have a nice day!')
    return ConversationHandler.END


# main function
def main():
    updater = Updater(API_key,use_context=True)
    dispatcher = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            'ORDERING': [MessageHandler(Filters.text, intent_extraction)],
            'ADD_INFO': [MessageHandler(Filters.text, add_info)],
            'SHOW_MENU': [MessageHandler(Filters.text, show_menu)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)
    
    updater.start_polling()
    updater.idle()

# call main function
if __name__ == '__main__':
    main()
