import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp(u'A severe storm hit the beach. It started to rain.')

# break each sentence in the document up into a list of tokens
for sent in doc.sents:
    print([sent[i] for i in range(len(sent))])

print('\n')

# to print each sentence in the document as-is (not as tokens, like above)
for sent in doc.sents:
    print([sent])

print('\n')

# you can access the tokens of a multi sentence text using normal doc indexing
print([doc[i] for i in range(len(doc))]) 

print('\n')

# see if the first word of the second sentence is a pronoun (can be useful for figuring out
# what the antecedent of a pronoun is)
for i, sent in enumerate(doc.sents):        # use enumerator in for loop
    if i == 1 and sent[0].pos_ == 'PRON':
        print('The second sentence begins with a pronoun.')


print('\n')

# see how many sentences in the document end with a verb
counter = 0

# the index of the last word in a sentence is at len(sent)-2, since it accounts for the punctuation
# at the end of each sentence
for sent in doc.sents:
    if sent[len(sent)-2].pos_ == 'VERB':
        counter+=1

print(counter)