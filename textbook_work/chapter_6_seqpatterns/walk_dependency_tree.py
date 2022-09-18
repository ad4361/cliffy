import spacy
nlp = spacy.load('en_core_web_sm')

# function that walks a dependency tree from right to left, iterating "left" over the heads of tokens.
# it starts by searching for a GPE (geopolitical entity), the token 'to', and then seeing if the two are
#       semantically connected. 
def find_destination(doc):
    for i, token in enumerate(doc):
        # find GPE token, if it exists
        if token.ent_type != 0 and token.ent_type_ == 'GPE':
            while True:
                token = token.head          # iterate over the heads of tokens
                if token.text == 'to':      # GPE and 'to' are semantically connected
                    return doc[i].text      # GPE is the destination, return it
                if token.head == token:     # happens when a token.dep_ == 'ROOT', its head is itself
                    return 'Failed to determine'
    return 'Failed to determine'    # no GPE token found, no destination found


doc1 = nlp('I am going to the conference in Berlin.')
dest1 = find_destination(doc1)
if dest1 != 'Failed to determine':
    print('It seems the user wants a ticket to ' + dest1 + '.')
else:
    print('Failed to determine the user\'s destination.')


doc2 = nlp('I am going to the conference.')
dest2 = find_destination(doc2)
if dest2 != 'Failed to determine':
    print('It seems the user wants a ticket to ' + dest2 + + '.')
else:
    print('Failed to determine the user\'s destination.')

