import spacy
nlp = spacy.load('en_core_web_sm')

doc = nlp('The product sales hit a new record in the first quarter, with 18.6 million units sold.')

#for token in doc:
#    print(token.text, token.head.text)
#print('\n')

# extract the phrase containing the relevant numerical info from the text
phrase = ''
for token in doc:
    if token.pos_ == 'NUM':     # find first NUM token in doc
        while True:
            phrase = phrase + ' ' + token.text
            token = token.head
            if token not in list(token.head.lefts):   # activated when main word of phrase is found
                phrase = phrase + ' ' + token.text    # full phrase has now been found
                break   # break from while loop
        break   # break from for loop




# at the start of this loop, token = 'units'
while True:
    token = token.head
    if token.pos_ != 'ADP':
        phrase = token.text + phrase
    if token.dep_ == 'ROOT':
        break
# at the end of this loop, token = 'hit', the ROOT verb


# now find the ROOT's subject and add it and its left children to the start of the phrase
for tok in token.lefts:
    if tok.dep_ == 'nsubj':
        phrase = ' '.join([tok.text for tok in tok.lefts]) + ' ' + tok.text + ' ' + phrase + '.'
        break
print(phrase)








