import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp('I want a dish.')

# extract transitive verb/dobj
for token in doc:
    if token.dep_ == 'dobj':
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


# replace the trans verb and dobj with synonyms supported by the application (the syns at top of list)
# to compose the string that expressed the intent
if len(verbSynonyms) == 0 or len(dobjSynonyms) == 0:
    intent = 'unrecognized'
else:
    intent = verbSynonyms[0][0] + dobjSynonyms[0][0].capitalize()
print(intent)

