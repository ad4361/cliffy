# identify intent to buy a plane ticket to San Francisco using given discourse
# aka: ['fly', 'San Francisco']

import spacy
nlp = spacy.load('en_core_web_sm')

from spacy.symbols import ORTH, LEMMA
special_case = [{ORTH: u'Frisco', LEMMA: u'San Francisco'}]
nlp.tokenizer.add_special_case(u'Frisco', special_case)

doc = nlp(u'I have flown to LA. Now I am flying to Frisco.')

# see if the ROOT token in a sentence is a present progressive verb. if it's not, discard sentence.
# if it is, then iterate over the sentence and, in a list, print all the ROOT VBG tokens 
# and pobj tokens 
for sent in doc.sents:
    for w in sent:
        if w.dep_ == 'ROOT' and w.tag_ == 'VBG':
            print([w.lemma_ for w in sent if w.dep_ == 'ROOT' and w.tag_ == 'VBG' 
                or w.dep_ == 'pobj' and w.head.head.tag_ == 'VBG'])
