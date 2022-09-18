import spacy
# intent is spread across multiple sentences. need to replace pronoun with antecedent

nlp = spacy.load('en_core_web_sm')
doc = nlp('I have finished my pizza. I liked it a lot. I want another one.')

# recognized intent words and synonyms
verbList = [('order', 'want', 'make', 'give'),
            ('show', 'find')]
dobjList = [('pizza', 'pie', 'dish'),
            ('cola', 'soda')]


# list of allowable substitutes for direct object
substitutes = ('one', 'it', 'same', 'more')

# dictionary for storing intent definition parts
intent = {'verb': '', 'dobj': ''}

# iterate over sentences
for sent in doc.sents:
    # iterate over the tokens in a sentence
    for token in sent:
        if token.dep_ == 'dobj':    # search for dobj
            # we are not interested in the tverb or dobj if they are not in the allowable word list
            verbSynonyms = [item for item in verbList if token.head.text in item] # token.head = tverb
            # determine if the dobj is in the dobjSynonyms list or the substitutes list
            dobjSynonyms = [item for item in dobjList if token.text in item]
            substitute = [item for item in substitutes if token.text in item]

            # if both a dobj and tverb were extracted:
            if (dobjSynonyms != [] or substitute != []) and verbSynonyms != []:
                # extract tverb
                intent['verb'] = verbSynonyms[0][0]
            # if a non-proform dobj was extracted:
            if dobjSynonyms != []:
                # extract dobj, which should be the antecedent
                intent['dobj'] = dobjSynonyms[0][0]

# compose the intent identifier:
intentStr = intent['verb'] + intent['dobj'].capitalize()
print(intentStr)