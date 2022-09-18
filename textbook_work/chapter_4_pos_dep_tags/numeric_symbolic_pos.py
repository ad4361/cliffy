import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp('The firm earned $1.5 million in 2017.')

# reminder: token.pos_ -> coarse grained part of speech
#           token.tag_ -> fine grained part of speech

for token in doc:
    print(token.text, token.pos_, spacy.explain(token.pos_))
# spacy.explain() returns a description for a given linguistic feature

print('\n')

for token in doc:
    print(token.text, token.pos_, token.tag_, spacy.explain(token.tag_))
