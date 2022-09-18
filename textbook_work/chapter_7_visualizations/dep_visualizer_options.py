import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_sm')
doc = nlp('I want a Greek pizza.')

# change visualizer to compact mode, change the font, and treat noun phrases as one token
options = {'compact': True, 'font': 'Tahoma', 'collapse_phrases': False, 'fine_grained': True}
displacy.serve(doc, style='dep', options=options)