import spacy
nlp = spacy.load('en_core_web_sm') # creates spaCy Language class, which has vocab and statmodel data
doc = nlp(u'I am flying to Frisco') # Doc obj: container for sequence of Token objs; generated implicitly

# with above 3 lines of code, spacy has generated the grammatical structure for the sentence

print([w.text for w in doc])