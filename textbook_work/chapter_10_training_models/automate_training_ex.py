from __future__ import annotations
import spacy

nlp = spacy.load('en_core_web_sm')

# to take utterances from a file called test.txt and put them into a doc object:
# f = open('test.txt', 'rb')
# contents = f.read()
# doc = nlp(contents.decode('utf8'))

doc = nlp('Could you send a taxi to Solnce? I need to get to Google. Could you send a taxi an hour later?')

training_examples = []

districts = ['Solnce', 'Greenwal', 'Downtown']

for sent in doc.sents:
    entities = []
    for token in sent:
        if token.ent_type != 0 or token.text in districts: # token is a named entity or in districts
            # token.idx: start index of a token in a doc
            # sent.start_char: start index of a sentence in a doc
            start = token.idx - sent.start_char     # token start index in sentence
            end = start + len(token)                # token end index in sentence

            if token.text in districts:
                entity = (start, end, 'GPE')
            else:
                entity = (start, end, token.ent_type_)
            entities.append(entity)
    sent_tuple = (sent.text, {'entities': entities})
    training_examples.append(sent_tuple)

#print(training_examples)


# now that we've created the training examples, let's disable the other pipeline components 
# before we start training the entity recognizer
# nlp.disable_pipes('tagger')
# nlp.disable_pipes('parser')
other_pipes = [pipe_name for pipe_name in nlp.pipe_names if pipe_name != 'ner']
nlp.disable_pipes(*other_pipes)


# processing training examples in batches
import random
from spacy.util import minibatch, compounding

# optimizer is a function that will be used during the training process to hold intermediate
# results between updates of the model weights. use the optimizer to update an existing model
optimizer = nlp.entity.create_optimizer()

for i in range(25):
    random.shuffle(training_examples)
    max_batch_size = 3
    batch_size = compounding(2.0, max_batch_size, 1.001)
    batches = minibatch(training_examples, size=batch_size)
    for batch in batches:
        texts, annotations = zip(*batch)
        nlp.update(texts, annotations, sgd=optimizer)
ner = nlp.get_pipe('ner')
ner.to_disk('/Users/adrie/AppData/Local/Programs/Python/Python38/lib/site-packages/en_core_web_sm/en_core_web_sm-2.3.1')



