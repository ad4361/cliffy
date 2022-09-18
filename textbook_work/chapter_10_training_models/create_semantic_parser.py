from __future__ import annotations
import spacy

# create a parser that labels tokens based on their semantic relations to other tokens, instead of
# by their syntactic dependencies on other tokens

# each element in the training_data list has this format:
# ('sentence text', {annotations})
#       where annotations = 
#           {'heads': [index of each token's head (integer)], 
#           'deps': [semantic label for each token (string)]}
TRAINING_DATA = [
    #  0   1   2    3     4    5   6     7
    ('find a high paying job with no experience',
    {'heads': [0, 4, 4, 4, 0, 7, 7, 4],
    'deps': ['ROOT', '-', 'QUALITY', 'QUALITY', 'ACTIVITY', '-', 'QUALITY', 'ATTRIBUTE']}),

    #  0    1      2      3      4    5
    ('find good workout classes near home',
    {'heads': [0, 3, 3, 0, 5, 3],
    'deps': ['ROOT', 'QUALITY', 'QUALITY', 'ACTIVITY', 'QUALITY', 'ATTRIBUTE']})
]


# this code is just to prove that SYNTACTICALLY related words may not be SEMANTICALLY related in our
# new parser
# nlp = spacy.load('en_core_web_sm')
# doc = nlp('find a high paying job with no experience')
# heads = []
# for token in doc:
#    heads.append(token.head.i)
# print(heads) 



nlp = spacy.blank('en')
parser = nlp.create_pipe('parser')
nlp.add_pipe(parser, first=True)

# extract each label from each training example, and add the labels to the parser
for text, annotations in TRAINING_DATA:
    for d in annotations.get('deps', []):
        parser.add_label(d)


optimizer = nlp.begin_training()
# note: if we were training an existing component instead of training from scratch, we would use
#       optimizer = nlp.entity.create_optimizer()


import random
for i in range(25):
    random.shuffle(TRAINING_DATA)
    for text, annotations in TRAINING_DATA:
        nlp.update([text], [annotations], sgd=optimizer)
parser.to_disk('/Users/adrie/AppData/Local/Programs/Python/Python38/lib/site-packages/en_core_web_sm/en_core_web_sm-2.3.1')


