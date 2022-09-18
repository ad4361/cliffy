import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp('I want a pizza and cola.')

# extract the dobj and the conjunct associated with it
#       (the conjunct of a noun is another noun joined to it by a conjunction such as "and" or "or")
for token in doc:
    if token.dep_ == 'dobj':
        tverb = token.head
        dobj = [token.text]     # we're placing it in a list so we can join it with another list later
        conj = [t.text for t in token.conjuncts]        # list of the dobj's conjuncts
# combine lists
dobj_conj = dobj + conj


print(dobj_conj)
# prints ['pizza', 'cola']
print(tverb)
print('\n')



# find the conjuncts of a noun without using token.conjuncts
for token in doc:
    if token.dep_ == 'dobj':
        tverb = token.head
        dobj = [token.text]
        conj = []
        for tkn in token.rights:
            if tkn.dep_ == 'conj':
                conj.append(tkn.text)

# combine lists
dobj_conj = dobj + conj


print(dobj_conj)
# prints ['pizza', 'cola']
print(tverb)