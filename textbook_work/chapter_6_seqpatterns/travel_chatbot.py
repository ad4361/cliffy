import spacy
nlp = spacy.load('en_core_web_sm')

# function that walks a dependency tree from right to left, iterating "left" over the heads of tokens.
# it starts by searching for a GPE (geopolitical entity), the token 'to', and then seeing if the two are
#       semantically connected. 
def dep_destination(doc):
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


# function the searches a doc for a GPE token. if a GPE token is found, it's returned. otherwise,
#       a 'failure to determine' message is returned 
def guess_destination(doc):
    for token in doc:
        if token.ent_type != 0 and token.ent_type_ == 'GPE':    
            return token.text   # GPE token found and returned
    return 'Failed to determine'    # no GPE token found


# generates and returns a response to an utterance based on the results of the above two functions.
# three scenarios:
#       scenario 1: user's intent and destination is obvious
#       scenario 2: user's intent is a little unclear
#       scenario 3: no user intent recognized
def gen_response(doc):
    dest = dep_destination(doc)
    if dest != 'Failed to determine':
        # scenario 1
        return 'When do you need to be in ' + dest + '?'

    dest = guess_destination(doc)
    if dest != 'Failed to determine':
        # scenario 2
        return 'Would you like a ticket to ' + dest + '?'

    # scenario 3
    return 'Are you flying somewhere?'

        
# scenario 1: 'to' + GPE pattern
doc1 = nlp('I am going to the conference in Berlin.')
print(gen_response(doc1) + '\n')

# scenario 2: GPE specified, but no 'to' token preceding it
doc2 = nlp('I am attending the conference in Berlin.')
print(gen_response(doc2) + '\n')

# scenario 3: no GPE specified
doc3 = nlp('I would like a plane ticket.')
print(gen_response(doc3) + '\n')



