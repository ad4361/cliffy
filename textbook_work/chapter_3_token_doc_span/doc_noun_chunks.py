import spacy
nlp = spacy.load('en_core_web_sm')

doc = nlp(u'A noun chunk is a phrase that has a noun as its head.')
for chunk in doc.noun_chunks:
    print(chunk)

print('\n')

# here's how to extract noun chunks from a sentence manually: using syntactic children
for token in doc:
    if token.pos_ == 'NOUN':
        chunk = ''
        for w in token.children:
            if w.pos_ == 'DET' or w.pos_ == 'ADJ': #if token is an adjective or determinant
                chunk = chunk + w.text + ' ' #add token to string
        chunk = chunk + token.text #add on noun which formed the head
        print(chunk) 

print('\n')

# note: for nouns, the words that modify them (determinants and adjectives) are always on the left
# side of the noun. so, modifying the above code:
for token in doc:
    if token.pos_ == 'NOUN':
        chunk = ''
        for w in token.lefts:
            chunk = chunk + w.text + ' ' #add token to string
        chunk = chunk + token.text #add on noun which formed the head
        print(chunk) 
# prints the same thing as the preceding two sections of code