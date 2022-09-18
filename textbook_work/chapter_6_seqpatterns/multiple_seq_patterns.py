import spacy
nlp = spacy.load('en_core_web_sm')

# function that checks if an input sentence follows the word sequence pattern for dependency labels:
# subject + auxiliary verb + verb + ... + direct object + ...
def dep_pattern(doc):
    # iterate over sentence, excluding end mark:
    for i in range(len(doc)-1):
        # if subject + auxiliary verb + verb detected:
        if doc[i].dep_ == 'nsubj' and doc[i+1].dep_ == 'aux' and doc[i+2].dep_ == 'ROOT':
            # if verb has a direct object child, return True
            for token in doc[i+2].rights:
                if token.dep_ == 'dobj':
                    return True
        # if pattern not matched, return False
        return False


# function that checks if an input sentence follows the word sequence pattern for parts of speech:
# personal pronoun + modal verb + base form verb + ... + personal pronoun + ...
def pos_pattern(doc):
    for token in doc: 
        # subject of sentence is not a personal pronoun, pos sequence mismatch
        if token.dep_ == 'nsubj' and token.tag_ != 'PRP':
            return False
        # auxiliary verb of sentence is not modal, pos sequence mismatch
        if token.dep_ == 'aux' and token.tag_ != 'MD':
            return False
        # root verb of sentence is not in its base form, pos sequence mismatch
        if token.dep_ == 'ROOT' and token.tag_ != 'VB':
            return False
        # direct object of sentence is not a personal pronoun, pos sequence mismatch
        if token.dep_ == 'dobj' and token.tag_ != 'PRP':
            return False
    # no pos sequence mismatches, pos pattern matched
    return True
        

doc1 = nlp('We can overtake them.')
doc2 = nlp('I might send them a card as a reminder.')

if dep_pattern(doc1) and pos_pattern(doc1):
    print('Input matches both patterns')
else:
    print('Input does not match both patterns')


if dep_pattern(doc2) and pos_pattern(doc2):
    print('Input matches both patterns')
else:
    print('Input does not match both patterns')

