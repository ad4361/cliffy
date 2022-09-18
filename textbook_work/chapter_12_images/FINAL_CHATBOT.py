import spacy
import wikipedia
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from textbook_work.chapter_11_deploy_chatbot.api_IGNORE import API_key


## HELPER FUNCTIONS

def keyphrase(doc):
    """
    Takes a sentence as a Doc object and extracts the most informative word or phrase from it.
    """
    # case: sentence has a preposition and pobj: pobj and its modifiers are the keyword(s)
    for token in doc:
        if token.dep_ == 'pobj' and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN'):
            phrase = (' '.join([child.text for child in token.lefts]) + ' ' + token.text).lstrip()
            return phrase
        
    # case: sentence has no prepositional phrase, but has a nsubj and verb that form keywords (and
    # possibly a dobj and its modifiers)
    for token in reversed(doc):
        if token.dep_ == 'nsubj' and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN'):
            nsubj = token.text
            verb = token.head

            # nsubj's modifiers (non-determinant):
            modifiers = ' '.join([child.text for child in token.lefts if child.dep_ != 'det'])
            dobj = ''
            for child in verb.children:
                if child.dep_ == 'dobj':
                    dobj = child.text
                    break

            return (modifiers + ' ' + nsubj + ' ' + verb.text + ' ' + dobj).lstrip()

    # case: sentence has no prep phrase, no appropriate nsubj and verb, but has a transitive verb and
    #       dobj that form keywords
    for token in reversed(doc):
        if token.dep_ == 'dobj' and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN'):
            phrase = token.head.lemma_ + 'ing ' + token.text
            return phrase
    
    # unable to determine keyword(s)
    return False
    

def wiki(concept):
    """
    Takes in a keyword or keyphrase and returns a sentence closely related to the keyword(s), using
    info from Wikipedia
    """

    nlp = spacy.load('en_core_web_sm')
    wiki_article = wikipedia.page(concept)
    doc = nlp(wiki_article.content)

    if len(concept.split()) == 1:
        for sent in doc.sents:
            for token in sent:
                if token.text == 'concept' and token.dep_ == 'dobj':
                    return sent.text
    
    return list(doc.sents)[0].text




## CHATBOT CALLBACK FUNCTIONS

# callback for /start CommandHandler
def start(update, context):
    update.message.reply_text('Hi! This is a conversational bot. Ask me something using a \
        complete sentence.')


# callback for text messages handler
def text_msg(update, context):
    msg = update.message.text
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(msg)

    concept = keyphrase(doc)
    if concept:
        update.message.reply_text('Phrase: ' + concept + '\n' + wiki(concept))
    else:
        update.message.reply_text('Please rephrase your question.')



def main():
    updater = Updater(API_key, use_context=True)
    
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, text_msg))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


    
