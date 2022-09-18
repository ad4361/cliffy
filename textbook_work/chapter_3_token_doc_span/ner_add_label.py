from __future__ import annotations
import spacy
nlp = spacy.load('en_core_web_sm')


doc = nlp('I need a taxi to Festy.')
for ent in doc.ents:
    print(ent.text, ent.label_)
# we want to customize our entity recognizer (ner) to recognize 'Festy' as a DISTRICT (a label that does
# not yet exist within the ner) instead of ORG (its default label)

# preparing the data necessary to do so:
LABEL = 'DISTRICT'
# you will need more than 2 examples, this is just a small example though  
TRAIN_DATA = [
    ('We need to deliver it to Festy.',         # example text w/ entity    # TEXT
        {'entities': [(25, 30, 'DISTRICT')]}),  # start index, end index (exclusive), label  # ANNOTATIONS
    ('I like oranges.',        # example text w/o entity                    # TEXT
        {'entities': []})      # no keyword, so no specifications           # ANNOTATIONS
]


# get the entity recognizer instance (of class EntityRecognizer) from nlp
ner = nlp.get_pipe('ner')

# add new label to ner
ner.add_label(LABEL)

# disable all other pipeline components so they aren't affected by training below
nlp.disable_pipes('tagger')
nlp.disable_pipes('parser')

# train your entity recognizer for new label
optimizer = nlp.entity.create_optimizer()
import random   # randomness is so statistical model won't be influenced by order of training examples

for i in range(25):
    random.shuffle(TRAIN_DATA)
    for text, annotations in TRAIN_DATA:
        nlp.update([text], [annotations], sgd=optimizer)



# test how the updated ner recognizes 'Festy'
doc = nlp('I need a taxi to Festy.')        # this line is impt, otherwise Festy is still an ORG
for ent in doc.ents:
    print(ent.text, ent.label_)


# to save these ner updates without having to run the training data examples every time, you can 
# serialize the ner to your disk
# this path is taken from the manual_spacy_load.py file
ner.to_disk('/Users/adrie/AppData/Local/Programs/Python/Python38/lib/site-packages/en_core_web_sm/en_core_web_sm-2.3.1')