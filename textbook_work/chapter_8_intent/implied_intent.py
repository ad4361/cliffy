import spacy

nlp = spacy.load('en_core_web_lg')
doc = nlp('I feel like eating a pie.')

# find dobj token
dobj = ''
for token in doc:
    if token.dep_ == 'dobj':
        dobj = token

# create a token for the word food (need to use a Doc object to do this)
tokens = nlp('food')

# calculate semantic similarity btwn dobj and tokens[0] = food. if above a certain threshold, user is
# probably trying to place an order, so ask relevant clarifying question
question = ''
if dobj.similarity(tokens[0]) > 0.4:
    question = 'Would you like to look at our menu?'

print(question)