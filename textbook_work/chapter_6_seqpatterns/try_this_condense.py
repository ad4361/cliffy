import spacy
nlp = spacy.load('en_core_web_sm')

doc = nlp('The company, whose profits reached a record high this year, largely attributed to changes in management, earned a total revenue of $4.26 million.')

#for token in doc:
#    print(token.text, token.head.text, token.head.pos_)
#print('\n')

phrase = ''

for token in doc: 
    if token.tag_ == '$':
        i = token.i
        token = doc[i+1]
        while True:
            phrase = phrase + ' ' + token.text
            token = token.head
            if token not in list(token.head.lefts):   # activated when main word of phrase is found
                phrase = phrase + ' ' + token.text    # full phrase has now been found
                break   # break from while loop
        break   # break from for loop
phrase = '$' + phrase.strip()   # removes whitespace at beginning of phrase


# at the start of this loop, token = 'million'
while True:
    token = token.head
    phrase = token.text + ' ' + phrase
    if token.dep_ == 'ROOT':
        break
# at the end of this loop, token = 'earned', the ROOT verb


# now find the ROOT's subject and add it and its left children to the start of the phrase
for tok in token.lefts:
    if tok.dep_ == 'nsubj':
        phrase = ' '.join([tok.text for tok in tok.lefts]) + ' ' + tok.text + ' ' + phrase + '.'
        break
print(phrase)


