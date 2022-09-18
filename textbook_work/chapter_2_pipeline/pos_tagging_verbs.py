# trying to see if customer intends to buy a ticket to a destination

import spacy
from spacy.symbols import ORTH, LEMMA

nlp = spacy.load('en_core_web_sm')
doc = nlp(u'I have flown to LA. Now I am flying to Frisco.')

# if a verb is tagged with VB (infinitive) or VBG (present progressive),
# it's likely (NOT CERTAIN) that the customer wants to buy a ticket 
print([w.text for w in doc if w.tag_ == 'VBG' or w.tag_ == 'VB'])

# spaCy tags part of speech other than verbs: ex, proper nouns
print([w.text for w in doc if w.pos_ == 'PROPN'])

