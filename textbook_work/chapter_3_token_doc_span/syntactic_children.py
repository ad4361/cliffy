import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp(u'I want a green apple')

# print left syntactic children of apple
print([w.text for w in doc[4].lefts])

# print all syntactic children of apple (note it's the same as above)
print([w.text for w in doc[4].children])

# print right syntactic children of want
print([w.text for w in doc[1].rights])

# print left syntactic children of want
print([w.text for w in doc[1].lefts])

# print all syntactic children of want
print([w.text for w in doc[1].children])

