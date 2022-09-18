import spacy
nlp = spacy.load('en_core_web_sm')

# compare two sentences to see if they share a dependency pattern

# same number of words allows for a simple for loop 
doc1 = nlp('We can overtake them.')
doc2 = nlp('You must specify it.')

# excluding closing punctuation mark
for i in range(len(doc1)-1):
    if doc1[i].dep_ == doc2[i].dep_:
        print(doc1[i].text, doc2[i].text, doc1[i].dep_, spacy.explain(doc1[i].dep_))


# including both sentences in one doc
print('\n')
doc3 = nlp('We can overtake them. You must specify it.')
sents = list(doc3.sents)

# note that this approach only works because we know there are 2 sentences in the doc,
# and that they are of the same length
for i in range(len(sents[0])-1):
    if sents[0][i].dep_ == sents[1][i].dep_:
        print(sents[0][i].text, sents[1][i], sents[0][i].dep_, spacy.explain(sents[0][i].dep_))

