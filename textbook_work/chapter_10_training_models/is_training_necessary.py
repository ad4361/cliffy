import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp('Could you pick me up at Solnce?')
# we want the ner to recognize Solnce as a GPE: does it already?

for ent in doc.ents:
    print(ent.text, ent.label_)
# nothing prints: it doesn't recognize Solnce as a named entity at all