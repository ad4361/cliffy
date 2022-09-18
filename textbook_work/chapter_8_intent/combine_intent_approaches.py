import spacy

nlp = spacy.load('en_core_web_lg')
doc = nlp('I feel like eating a pie.')

# extract transitive verb/dobj
for token in doc:
    if token.dep_ == 'dobj':
        dobj_token = token
        dobj = token.text
        verb = token.head.text

# create a list of tuples for possible verb synonyms
verbList = [('order', 'want', 'give', 'make'), 
            ('show', 'find')]

# find the tuple containing the transitive verb that was extracted above
verbSynonyms = [item for item in verbList if verb in item]



# create a list of tuples for possible direct object synonyms
dobjList = [('pizza', 'pie', 'dish'),
            ('cola', 'soda')]

# find the tuple containing the dobj that was extracted above
dobjSynonyms = [item for item in dobjList if dobj in item]


if len(verbSynonyms) != 0 and len(dobjSynonyms) != 0:
    # hardcoded synonyms approach succeeded in intent identification
    intent = verbSynonyms[0][0] + dobjSynonyms[0][0].capitalize()
    print(intent)

else:   # clarifying question required: use semantic similarity
    tokens = nlp('food')
    question = ''
    if dobj_token.similarity(tokens[0]) > 0.4:
        print('Would you like to look at our menu?')
    else:
        print('Intent not recognized')