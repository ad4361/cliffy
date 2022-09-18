import spacy
from spacy.tokens.doc import Doc
from spacy.vocab import Vocab

# you can create a Doc object using its constructor 
doc = Doc(Vocab(), words=[u'Hi', u'there'])
print(doc)

# or the way we've been using:
# nlp = spacy.load('en_core_web_sm')
# doc = nlp(u'Hi there')
