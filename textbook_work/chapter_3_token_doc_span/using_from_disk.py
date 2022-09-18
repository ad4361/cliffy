import spacy
from spacy.pipeline import EntityRecognizer

nlp = spacy.load('en_core_web_sm', disable=['ner'])
ner = EntityRecognizer(nlp.vocab)
# path from ner_add_label.py file
ner.from_disk('/Users/adrie/AppData/Local/Programs/Python/Python38/lib/site-packages/en_core_web_sm/en_core_web_sm-2.3.1')
nlp.add_pipe(ner)

# test ner component to see if it has the DISTRICT label created in ner_add_label.py
doc = nlp('We need to deliver it to Festy.')
for ent in doc.ents:
    print(ent.text, ent.label_)
# IT WORKS!!!!!!

