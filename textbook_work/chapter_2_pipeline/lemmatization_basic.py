import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp(u'this product integrates both libraries for downloading and applying patches')

for token in doc:
    print(token.text, token.lemma_)