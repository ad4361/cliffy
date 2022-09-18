import spacy
nlp = spacy.load('en_core_web_sm')

doc = nlp('The firm earned $1.5 million in 2017, in comparison with $1.2 million in 2016.')
phrase = ''

for token in doc:
    if token.tag_ == '$':
        phrase = token.text
        i = token.i + 1     # i is the index of the token after the '$' token
        while doc[i].tag_ == 'CD':      # checks if the token(s) after '$' are cardinal numbers
            phrase += doc[i].text + ' '     # add cardinal numbers to phrase
            i += 1
        print(phrase)
