import spacy
from spacy.pipeline import EntityRecognizer

nlp = spacy.load('en_core_web_sm', disable=['ner']) # disable entity recognizer in pipeline
ner = EntityRecognizer(nlp.vocab) # create entity recognizer from constructor
ner.from_disk('/Users/adrie/AppData/Local/Programs/Python/Python38/lib/site-packages/en_core_web_sm/en_core_web_sm-2.3.1')
nlp.add_pipe(ner, 'custom_ner')

print(nlp.meta['pipeline'])

doc = nlp('Could you pick me up at Solnce?')
for ent in doc.ents:
    print(ent.text, ent.label_)
# Solnce should be recognized as a GPE, and it is :)