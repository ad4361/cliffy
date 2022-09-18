import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp(u'I have flown to LA. Now I am flying to Frisco.')

# to see parts of speech and dependency labels:
for token in doc:
    print(token.text, token.pos_, token.dep_)

print("\n")

# to see dependency arcs in the discourse: head dep child
for token in doc:
    print(token.head.text, token.dep_, token.text)

print("\n")

# in our case, the two words that are key to intent recognition in this discourse are 
# the tokens with the dependency labels ROOT and pobj (flying, LA, Frisco)
for sent in doc.sents:
    print([w.text for w in sent if w.dep_ == 'ROOT' or w.dep_ == 'pobj'])

