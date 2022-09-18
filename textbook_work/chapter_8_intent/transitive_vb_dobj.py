import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp('show me the best hotel in berlin')

# reminder: the head of a dobj token is a transitive verb token 

for token in doc:
    if token.dep_ == 'dobj':
        print(token.head.text + token.text.capitalize())
        # prints showHotel, which is an intent identifier