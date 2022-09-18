import spacy
import wikipedia
from cliffy_IGNORE import telegramAPI_key
from summarize import summarize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

## HELPER FUNCTIONS

def keyphrase(doc):
    """
    Takes a sentence as a Doc object and extracts the most informative word or phrase from it.
    """
    # case: sentence has a preposition and pobj: pobj and its modifiers are the keyword(s)
    for token in doc:
        if token.dep_ == 'pobj' and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN'):
            phrase = (' '.join([child.text for child in token.lefts]) + ' ' + token.text).lstrip()

            # check the pobj's right children. if one of them is a prepositon, pick it up and 
            #   its respective pobj, and add them to the phrase
            # bool() evaluates to True on non-empty lists
            if bool([rchild for rchild in token.rights if rchild.dep_ == 'prep']):
                prep = list(token.rights)[0]
                pobj = list(prep.children)[0]
                phrase = phrase + ' ' + prep.text + ' ' + pobj.text

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



def wiki(keyphrase):
    """
    Takes in a keyword or keyphrase and returns a sentence closely related to the keyword(s), using
    info from Wikipedia
    """

    nlp = spacy.load('en_core_web_lg')
    keyphrase_doc = nlp(keyphrase) # used for semantic similarity calculations

    # list of relevant article titles
    relevant_article_titles = wikipedia.search(keyphrase)
    print(relevant_article_titles)
    
    # compare semantic similarities between concept phrase and article titles
    #   -> one with highest similarity value gets chosen
    titles_similarity = {}
    for title in relevant_article_titles:
        title_doc = nlp(title)
        titles_similarity[title] = keyphrase_doc.similarity(title_doc)
    article_title = max(titles_similarity, key=titles_similarity.get)
    
    #summary = wikipedia.summary(article_title, sentences=2, auto_suggest=False)
    article_text = wikipedia.page(article_title).content
    doc = nlp(article_text)
    summary = summarize(doc)

    return summary



## CHATBOT CALLBACK FUNCTIONS

# callback for /start CommandHandler
def start(update, context):
    update.message.reply_text('Hi, my name is Cliffy! Ask me something using a \
complete sentence, and I\'ll find you an answer from Wikipedia.')

# callback for text messages handler
def text_msg(update, context):
    msg = update.message.text
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(msg)

    concept = keyphrase(doc)
    if concept:
        update.message.reply_text('Phrase: ' + concept + '\n' + wiki(concept) + '\n\nNot what you\'re looking for? Try rephrasing your question.')
    else:
        update.message.reply_text('Sorry, I didn\'t understand that. Please rephrase your question.')



def main():
    updater = Updater(telegramAPI_key, use_context=True)
    
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, text_msg))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

