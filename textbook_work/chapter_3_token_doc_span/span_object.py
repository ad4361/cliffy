import spacy
nlp = spacy.load('en_core_web_sm')

# doc[2:5] is a Span object, which is a slice of a Doc object
# doc.sents and doc.noun_chunks are also slices of a Doc object and thus are also Span objects
doc = nlp('I want a green apple.')
print(doc[2:5])
print('\n')
# REMINDER: python list slicing includes the element at the first specified index, and excludes the one 
# at the last specified index. so, in the above case, it includes the elements at the indices 2,3, and 4


# using doc.retokenize() method 

doc = nlp('The Golden Gate Bridge is an iconic landmark in San Francisco.')
print([doc[i] for i in range(len(doc))])
print('\n')

# we want 'Golden Gate Bridge' to be grouped together, since it is a multi-word entity name 
span = doc[1:4]
with doc.retokenize() as retokenizer:
    retokenizer.merge(span, attrs={"LEMMA": "Golden Gate Bridge"})

# now group 'San Francisco' together
span = doc[7:9]
with doc.retokenize() as retokenizer:
    retokenizer.merge(span, attrs={"LEMMA": "San Francisco"})

# print to show how the words have been grouped into a single token
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.dep_)
